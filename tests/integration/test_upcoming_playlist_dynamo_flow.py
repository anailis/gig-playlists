import logging
import json
import os
from datetime import date, timedelta

import boto3
import pytest
from botocore.exceptions import ClientError

logger = logging.getLogger()

EVENT_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "../resources/test_data/dynamodb_stream_events"
)
TEST_USER = "USER#ddd797f7-7b66-45ac-87a0-6604f52dc2fd"
TEST_ARTIST = "7oPftvlwr6VrsViSDV7fJY"
TEST_PLAYLIST = "70ZBZd7PC0g8f2gFg3kKGC"
SCHEDULE_NAME = f"delete_{TEST_ARTIST}_from_{TEST_PLAYLIST}"


def get_arn_from_stack(stack: dict, key: str) -> str:
    out = [out for out in stack if out["OutputKey"] == key]
    if not out:
        raise KeyError(f"{key} not found in stack gig-playlists")
    return out[0]["OutputValue"]


@pytest.fixture(scope="session")
def stack():
    client = boto3.client("cloudformation")
    response = client.describe_stacks(StackName="gig-playlists")
    return response["Stacks"][0]["Outputs"]


@pytest.fixture(scope="session")
def add_gig_lambda_arn(stack):
    return get_arn_from_stack(stack, "AddGigToUpcomingPlaylistFunctionArn")


@pytest.fixture(scope="session")
def remove_gig_lambda_arn(stack):
    return get_arn_from_stack(stack, "RemoveGigFromUpcomingPlaylistFunctionArn")


@pytest.fixture(scope="session")
def lambda_client():
    return boto3.client("lambda")


@pytest.fixture
def scheduler():
    yield boto3.client("scheduler")


def trigger_add_gig_lambda(lambda_client, arn, event):
    add_lambda_response = lambda_client.invoke(
        FunctionName=arn,
        Payload=json.dumps(event)
    )
    assert add_lambda_response["StatusCode"] == 200

    payload = json.load(add_lambda_response["Payload"])
    assert "errorMessage" not in payload, \
        f"Lambda AddGigToUpcomingPlaylist exited with error: {payload['errorMessage']}"
    assert len(payload) == 1, f"Unexpected payload: {payload}"
    assert TEST_USER in payload.keys(), "Playlist updated for wrong user"
    return payload


def trigger_remove_gig_lambda(lambda_client, arn, event):
    remove_lambda_response = lambda_client.invoke(
        FunctionName=arn,
        Payload=json.dumps(event)
    )
    assert remove_lambda_response["StatusCode"] == 200

    payload = json.load(remove_lambda_response["Payload"])
    assert "errorMessage" not in payload, \
        f"Lambda RemoveGigFromUpcomingPlaylist exited with error: {payload['errorMessage']}"
    assert payload["playlistId"] == TEST_PLAYLIST, "Artist removed from wrong playlist"
    assert payload["spotifyArtistId"] == TEST_ARTIST, "Wrong artist removed from playlist"
    return payload


def test_add_and_remove_future_gig(add_gig_lambda_arn, remove_gig_lambda_arn, lambda_client, scheduler):
    with open(os.path.join(EVENT_DIR, "create_gig.json")) as f:
        event = json.load(f)
    event["dynamodb"]["NewImage"]["date"]["S"] = (date.today() + timedelta(days=2)).strftime("%Y-%m-%d")
    dynamodb_stream = {"Records": [event]}

    payload = trigger_add_gig_lambda(lambda_client, add_gig_lambda_arn, dynamodb_stream)
    assert len(payload[TEST_USER]) == 1, f"Incorrect number of artists ({len(payload[TEST_USER])}) added to playlist"
    assert TEST_ARTIST == payload[TEST_USER][0], "Wrong artist added to playlist"
    try:
        scheduler.get_schedule(Name=SCHEDULE_NAME)
    except ClientError:
        pytest.fail("Delete schedule was not created")

    # Check idempotency of add gig function
    payload = trigger_add_gig_lambda(lambda_client, add_gig_lambda_arn, dynamodb_stream)
    assert len(payload[TEST_USER]) == 0, f"Artist was added to playlist again, creating duplicates in playlist"

    payload = trigger_remove_gig_lambda(
        lambda_client,
        remove_gig_lambda_arn,
        {"spotifyArtistId": TEST_ARTIST, "playlistId": TEST_PLAYLIST}
    )
    assert payload["removed"], "Artist not removed from playlist"

    # Check idempotency of remove gig function
    payload = trigger_remove_gig_lambda(
        lambda_client,
        remove_gig_lambda_arn,
        {"spotifyArtistId": TEST_ARTIST, "playlistId": TEST_PLAYLIST}
    )
    assert not payload["removed"], "Artist removed from playlist"

    # Clean-up deletion schedule
    scheduler.delete_schedule(Name=SCHEDULE_NAME)


def test_add_past_gig(add_gig_lambda_arn, lambda_client, scheduler):
    with open(os.path.join(EVENT_DIR, "create_gig.json")) as f:
        event = json.load(f)
    dynamodb_stream = {"Records": [event]}

    payload = trigger_add_gig_lambda(lambda_client, add_gig_lambda_arn, dynamodb_stream)
    assert len(payload[TEST_USER]) == 0

    with pytest.raises(ClientError):
        scheduler.get_schedule(Name=SCHEDULE_NAME)
