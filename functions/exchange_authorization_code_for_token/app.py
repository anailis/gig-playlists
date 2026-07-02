import json
import os

import boto3

from gigs_api import add_integration
from jwt import get_requesting_user
from oauth import get_refresh_token


kms_client = boto3.client("kms")
dynamodb_client = boto3.resource("dynamodb")
table = dynamodb_client.Table(os.environ["TABLE_NAME"])


def lambda_handler(event: dict, context):
    body = json.loads(event["body"])
    refresh_token = get_refresh_token(event_body=body)

    encrypted_refresh_token = kms_client.encrypt(
        KeyId=os.environ["KEY_ID"],
        Plaintext=refresh_token.encode(),
    )["CiphertextBlob"]

    add_integration(
        url=os.environ["INTEGRATIONS_API_URL"],
        user_id=get_requesting_user(event),
        encrypted_refresh_token=encrypted_refresh_token,
        jwt=event["headers"]["authorization"],
        scope=body["scope"],
        integration_type=body["type"]
    )

    return {"message": "Code exchanged for token successfully"}