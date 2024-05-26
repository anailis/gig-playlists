from datetime import date
from uuid import UUID, uuid4
import os

from aws_lambda_powertools.event_handler import APIGatewayHttpResolver, Response
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools import Logger
import boto3
from boto3.dynamodb.conditions import Key
from pydantic import BaseModel, Field

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])
app = APIGatewayHttpResolver(enable_validation=True)
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


@app.get("/users/<id>")
def get_user_by_id(user_id: str):
    results = table.query(KeyConditionExpression=Key("id").eq(USER_PREFIX + user_id))
    if results["Count"] == 0:
        # FIXME: give a proper response
        return Response(
            status_code=404,
            body="User not found"
        )
    else:
        return results


@app.get("/users/<id>/gigs")
def get_gigs_for_user(user_id: str):
    results = table.query(
        IndexName="userId-id-index",
        KeyConditionExpression=(
                Key("userId").eq(USER_PREFIX + user_id) &
                Key("id").begins_with(GIG_PREFIX)
        )
    )
    return results


@app.get("/gigs/<id>")
def get_gig_by_id(gig_id: str):
    results = table.query(KeyConditionExpression=Key("id").eq(GIG_PREFIX + gig_id))
    if results["Count"] == 0:
        # FIXME: give a proper response
        return Response(
            status_code=404,
            body="Gig not found"
        )
    else:
        return results


@app.post("/gigs")
def post_gig(gig: Gig):
    item: dict = gig.dict()
    item["date"] = gig.date.strftime("%Y-%m-%d")
    item["id"] = GIG_PREFIX + str(gig.id)
    table.put_item(Item=item)
    return "Created gig with ID " + str(gig.id)


def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
