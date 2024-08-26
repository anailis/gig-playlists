import boto3


from aws_lambda_powertools.utilities.data_classes import event_source
from aws_lambda_powertools.utilities.data_classes.api_gateway_authorizer_event import (
    APIGatewayAuthorizerTokenEvent,
    APIGatewayAuthorizerResponse,
)


ssm_client = boto3.client("ssm")


@event_source(data_class=APIGatewayAuthorizerTokenEvent)
def lambda_handler(event: APIGatewayAuthorizerTokenEvent, context):
    arn = event.parsed_arn

    policy = APIGatewayAuthorizerResponse(
        principal_id="user",
        region=arn.region,
        aws_account_id=arn.aws_account_id,
        api_id=arn.api_id,
        stage=arn.stage
    )

    expected_token = ssm_client.get_parameter(Name="/gigs/crud_api_token")["Parameter"]["Value"]
    if event.authorization_token == expected_token:
        policy.allow_all_routes()
    else:
        policy.deny_all_routes()
    return policy.asdict()
