import logging
import json
from datetime import date, timedelta

import boto3
import pytest
from botocore.exceptions import ClientError

logger = logging.getLogger()
EVENT_DIR = "resources/test_data/dynamodb_stream_events"
TEST_USER = "USER#ed9af2a7-60e5-448f-8081-9c49966d7f15"
TEST_ARTIST = "7oPftvlwr6VrsViSDV7fJY"
TEST_PLAYLIST = "70ZBZd7PC0g8f2gFg3kKGC"
SCHEDULE_NAME = f"delete_{TEST_ARTIST}_from_{TEST_PLAYLIST}"


@pytest.fixture(scope="session")
def lambda_arn():
    lambda_key = "AddGigToUpcomingPlaylistFunctionArn"
    client = boto3.client("cloudformation")
    response = client.describe_stacks(StackName="gig-playlists")

    stacks = response["Stacks"]
    stack_outputs = stacks[0]["Outputs"]
    api_outputs = [output for output in stack_outputs if output["OutputKey"] == lambda_key]

    if not api_outputs:
        raise KeyError(f"{lambda_key} not found in stack gig-playlists")

    return api_outputs[0]["OutputValue"]


@pytest.fixture(scope="session")
def lambda_client():
    return boto3.client("lambda")


@pytest.fixture
def scheduler():
    yield boto3.client("scheduler")


def test_add_future_gig(lambda_arn, lambda_client, scheduler):
    with open(f"{EVENT_DIR}/create_gig.json") as f:
        event = json.load(f)
    event["dynamodb"]["NewImage"]["date"]["S"] = (date.today() + timedelta(days=2)).strftime("%Y-%m-%d")
    dynamodb_stream = {"Records": [event]}

    response = lambda_client.invoke(
        FunctionName=lambda_arn,
        Payload=json.dumps(dynamodb_stream)
    )

    assert response["StatusCode"] == 200
    payload = json.load(response["Payload"])
    assert len(payload) == 1
    assert TEST_USER in payload.keys()
    assert len(payload[TEST_USER]) == 1
    assert TEST_ARTIST == payload[TEST_USER][0]

    try:
        scheduler.get_schedule(Name=SCHEDULE_NAME)
    except ClientError:
        pytest.fail("Delete schedule was not created")
    scheduler.delete_schedule(Name=SCHEDULE_NAME)

    # TODO: remove artist


def test_add_past_gig(lambda_arn, lambda_client, scheduler):
    with open(f"{EVENT_DIR}/create_gig.json") as f:
        event = json.load(f)
    dynamodb_stream = {"Records": [event]}

    response = lambda_client.invoke(
        FunctionName=lambda_arn,
        Payload=json.dumps(dynamodb_stream)
    )

    assert response["StatusCode"] == 200
    payload = json.load(response["Payload"])
    assert len(payload) == 1
    assert TEST_USER in payload.keys()
    assert len(payload[TEST_USER]) == 0

    with pytest.raises(ClientError):
        scheduler.get_schedule(Name=SCHEDULE_NAME)