import boto3


from aws_lambda_powertools.utilities.data_classes import event_source
from aws_lambda_powertools.utilities.data_classes.api_gateway_authorizer_event import (
    APIGatewayAuthorizerResponse, APIGatewayRouteArn, APIGatewayAuthorizerEventV2,
)


ssm_client = boto3.client("ssm")

def create_policy(arn: APIGatewayRouteArn) -> APIGatewayAuthorizerResponse:
    return APIGatewayAuthorizerResponse(
        principal_id="user",
        region=arn.region,
        aws_account_id=arn.aws_account_id,
        api_id=arn.api_id,
        stage=arn.stage
    )


def allow_access_for_valid_token(
        policy: APIGatewayAuthorizerResponse,
        provided_token: str,
        expected_token: str) -> None:
    if provided_token == expected_token:
        policy.allow_all_routes()
    else:
        policy.deny_all_routes()


@event_source(data_class=APIGatewayAuthorizerEventV2)
def lambda_handler(event: APIGatewayAuthorizerEventV2, context):
    expected_token = ssm_client.get_parameter(Name="/gigs/crud_api_token")["Parameter"]["Value"]
    policy = create_policy(event.parsed_arn)
    allow_access_for_valid_token(policy, event.headers.get("authorization"), expected_token)
    return policy.asdict()
