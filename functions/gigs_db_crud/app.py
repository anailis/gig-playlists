from datetime import date
from uuid import UUID, uuid4
import os

from aws_lambda_powertools.event_handler import APIGatewayRestResolver, CORSConfig
from aws_lambda_powertools.event_handler.exceptions import NotFoundError
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools import Logger
import boto3
from boto3.dynamodb.conditions import Key
from pydantic import BaseModel, Field

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

cors_config = CORSConfig(allow_origin="http://localhost:4200", max_age=300)
app = APIGatewayRestResolver(enable_validation=True, cors=cors_config)
logger = Logger()

GIG_PREFIX = "GIG#"
USER_PREFIX = "USER#"


class Gig(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    userId: str
    artist: str
    date: date
    venue: str
    spotifyArtistId: str


@app.get("/users/<user_id>", cors=True)
def get_user_by_id(user_id: str):
    results = table.query(KeyConditionExpression=Key("id").eq(USER_PREFIX + user_id))
    if results["Count"] == 0:
        raise NotFoundError
    else:
        return results["Items"]


@app.get("/users/<user_id>/gigs")
def get_gigs_for_user(user_id: str):
    results = table.query(
        IndexName="userId-id-index",
        KeyConditionExpression=(
                Key("userId").eq(USER_PREFIX + user_id) &
                Key("id").begins_with(GIG_PREFIX)
        )
    )
    return results["Items"]


@app.get("/gigs/<gig_id>")
def get_gig_by_id(gig_id: str):
    results = table.query(KeyConditionExpression=Key("id").eq(GIG_PREFIX + gig_id))
    if results["Count"] == 0:
        raise NotFoundError
    else:
        return results["Items"]


@app.post("/gigs")
def post_gig(gig: Gig):
    item: dict = gig.dict()
    item["date"] = gig.date.strftime("%Y-%m-%d")
    item["id"] = GIG_PREFIX + str(gig.id)
    table.put_item(Item=item)
    return {"message": "Created gig with ID " + str(gig.id)}


def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
