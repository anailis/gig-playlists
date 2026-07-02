import base64
import json
import os

import boto3
import requests
from aws_lambda_powertools import Logger
from requests import HTTPError

from jwt import get_requesting_user

logger = Logger()

kms_client = boto3.client("kms")
dynamodb_client = boto3.resource("dynamodb")
table = dynamodb_client.Table(os.environ["TABLE_NAME"])


def lambda_handler(event: dict, context):
    body = json.loads(event["body"])

    try:
        response = requests.post(
            body["refresh_token_uri"],
            data={
                "grant_type": "authorization_code",
                "client_id": body["client_id"],
                "code": body["code"],
                "redirect_uri": body["redirect_uri"],
                "code_verifier": body["code_verifier"],
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()
    except HTTPError as e:
        logger.error(e.response.status_code)
        logger.error(e.response.text)
        raise HTTPError

    refresh_token = response.json()["refresh_token"]

    response = kms_client.encrypt(KeyId=os.environ["KEY_ID"], Plaintext=refresh_token.encode())
    try:
        response = requests.post(
            os.environ["INTEGRATIONS_API_URL"],
            json={
                "userId": get_requesting_user(event),
                "type": body["type"],
                "refreshToken": base64.b64encode(response["CiphertextBlob"]).decode("utf-8"),
                "scope": body["scope"],
            },
            headers={"Authorization": event["headers"]["authorization"]},
        )
        response.raise_for_status()
    except HTTPError as e:
        logger.error(e.response.status_code)
        logger.error(e.response.text)
        raise HTTPError
    return "Code exchanged for token successfully"