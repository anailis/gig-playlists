import logging
import json

import boto3
import pytest
from botocore.exceptions import ClientError


logger = logging.getLogger()
EVENT_DIR = "resources/test_data/dynamodb_stream_events"


class TestApiGateway:

    @pytest.fixture(scope="session")
    def lambda_arn(self):
        lambda_key = "AddGigToUpcomingPlaylistFunctionArn"
        client = boto3.client("cloudformation")
        response = client.describe_stacks(StackName="gig-playlists")

        stacks = response["Stacks"]
        stack_outputs = stacks[0]["Outputs"]
        api_outputs = [output for output in stack_outputs if output["OutputKey"] == lambda_key]

        if not api_outputs:
            raise KeyError(f"{lambda_key} not found in stack gig-playlists")

        return api_outputs[0]["OutputValue"]

    def test_add_past_gig(self, lambda_arn):
        with open(f"{EVENT_DIR}/create_gig.json") as f:
            event = json.load(f)
        dynamodb_stream = {"Records": [event]}

        try:
            client = boto3.client("lambda")
            response = client.invoke(
                FunctionName=lambda_arn,
                Payload=json.dumps(dynamodb_stream)
            )
        except ClientError:
            logger.exception("Couldn't invoke function %s.", lambda_arn)
            raise

        assert response["StatusCode"] == 200
        # no change to playlist
        # no deletion scheduled
