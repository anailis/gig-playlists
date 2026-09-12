import os

from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.event_handler.exceptions import ForbiddenError, NotFoundError, BadRequestError
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools import Logger
import boto3

from gigs_db.gigs_db_service import GigsDbService, Gig, Integration

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])
db_service = GigsDbService(table)

app = APIGatewayHttpResolver(enable_validation=True)
logger = Logger()

GIG_PREFIX = "GIG#"
USER_PREFIX = "USER#"


def get_requesting_user() -> str:
    authoriser_details = app.current_event.get("requestContext", {}).get(
        "authorizer", {}
    )
    return authoriser_details.get("jwt", {}).get("claims", {}).get("sub", "")


@app.get("/users/<user_id>")
def get_user_by_id(user_id: str):
    if user_id != get_requesting_user():
        raise ForbiddenError("Forbidden: user cannot access this resource")
    user = db_service.get_user_by_id(user_id)
    if user is None:
        raise NotFoundError
    return user


@app.get("/users/<user_id>/gigs")
def get_gigs_for_user(user_id: str):
    if user_id != get_requesting_user():
        raise ForbiddenError("Forbidden: user cannot access this resource")
    return db_service.get_gigs_for_user(
        user_id
    )


@app.get("/gigs/<gig_id>")
def get_gig_by_id(gig_id: str):
    gig = db_service.get_gig_by_id(gig_id)
    if gig["userId"] != USER_PREFIX + get_requesting_user():
        raise ForbiddenError("Forbidden: user cannot access this resource")
    if gig is None:
        raise NotFoundError
    return gig


@app.post("/gigs")
def post_gig(gig: Gig):
    if gig.userId != USER_PREFIX + get_requesting_user():
        raise ForbiddenError("Forbidden: user cannot create gig for another user")
    return db_service.post_gig(gig)


@app.delete("/gigs/<gig_id>")
def delete_gig(gig_id: str):
    gig = db_service.get_gig_by_id(gig_id)
    if gig is None:
        raise NotFoundError
    if gig["userId"] != USER_PREFIX + get_requesting_user():
        raise ForbiddenError("Forbidden: user cannot access this resource")
    return db_service.delete_gig(gig["id"], gig["userId"])


@app.post("/integrations")
def post_integration(integration: Integration):
    if not integration.userId.startswith(USER_PREFIX):
        raise BadRequestError("Bad Request: userId must start with 'USER#'")
    if integration.userId != USER_PREFIX + get_requesting_user():
        raise ForbiddenError("Forbidden: user cannot create integration for another user")
    try:
        message = db_service.post_integration(integration)
    except ValueError:
        raise ForbiddenError(f"Forbidden: user already has an integration of type {integration.type}")
    return message


def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
