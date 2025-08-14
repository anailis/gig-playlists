from unittest.mock import Mock

import pytest
from aws_lambda_powertools.utilities.data_classes.api_gateway_authorizer_event import APIGatewayRouteArn

from gigs_db_auth.app import create_policy, allow_access_for_valid_token

EXPECTED_TOKEN = "validToken"

def test_create_policy_success():
    arn = APIGatewayRouteArn(
        region="us-east-1",
        aws_account_id="1234",
        api_id="api1234",
        stage="testing",
        http_method="GET",
        resource="myapi"
    )
    policy = create_policy(arn)

    assert policy.principal_id == "user"
    assert policy.region == "us-east-1"
    assert policy.aws_account_id == "1234"
    assert policy.api_id == "api1234"
    assert policy.stage == "testing"

@pytest.fixture()
def policy():
    return Mock()

def test_correct_token_given(policy):
    allow_access_for_valid_token(policy, "Bearer validToken", EXPECTED_TOKEN)

    policy.allow_all_routes.assert_called_once()
    policy.deny_all_routes.assert_not_called()

def test_incorrect_token_given(policy):
    allow_access_for_valid_token(policy, "Bearer invalidToken", EXPECTED_TOKEN)

    policy.allow_all_routes.assert_not_called()
    policy.deny_all_routes.assert_called_once()

def test_invalid_token_format_given(policy):
    allow_access_for_valid_token(policy, "Bearer invalidToken", EXPECTED_TOKEN)

    policy.allow_all_routes.assert_not_called()
    policy.deny_all_routes.assert_called_once()
