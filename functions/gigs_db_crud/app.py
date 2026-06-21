import os

from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools import Logger
import boto3

from gigs_db_service import GigsDbService, Gig

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])
db_service = GigsDbService(table)

app = APIGatewayHttpResolver(enable_validation=True)
logger = Logger()

GIG_PREFIX = "GIG#"
USER_PREFIX = "USER#"


def get_requesting_user() -> str:
    authoriser_details = app.current_event.get("requestContext", {}).get("authorizer", {})
    return authoriser_details.get("jwt", {}).get("claims", {}).get("sub", "")

@app.get("/users/<user_id>")
def get_user_by_id(user_id: str):
    return db_service.get_user_by_id(user_id, requesting_user_id=get_requesting_user())


@app.get("/users/<user_id>/gigs")
def get_gigs_for_user(user_id: str):
    return db_service.get_gigs_for_user(user_id, requesting_user_id=get_requesting_user())


@app.get("/gigs/<gig_id>")
def get_gig_by_id(gig_id: str):
    return db_service.get_gig_by_id(gig_id, requesting_user_id=get_requesting_user())


@app.post("/gigs")
def post_gig(gig: Gig):
    return db_service.post_gig(gig, requesting_user_id=get_requesting_user())


@app.delete("/gigs/<gig_id>")
def delete_gig(gig_id: str):
    return db_service.delete_gig(gig_id, requesting_user_id=get_requesting_user())


def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
