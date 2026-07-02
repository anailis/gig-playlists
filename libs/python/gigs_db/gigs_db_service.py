from datetime import date
from enum import StrEnum
from uuid import UUID, uuid4

from aws_lambda_powertools.event_handler.exceptions import NotFoundError, ForbiddenError
from boto3.dynamodb.conditions import Key
from pydantic import BaseModel, Field


class Gig(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    userId: str
    artist: str
    date: date
    venue: str
    spotifyArtistId: str


class IntegrationType(StrEnum):
    SPOTIFY = "SPOTIFY"
    TIDAL = "TIDAL"


class Integration(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    userId: str
    type: IntegrationType
    refreshToken: str
    scope: list


class GigsDbService:
    GIG_PREFIX = "GIG#"
    USER_PREFIX = "USER#"
    INTEGRATION_PREFIX = "INTEGRATION#"

    def __init__(self, table):
        self.table = table

    def get_user_by_id(self, user_id: str, requesting_user_id: str):
        if user_id != requesting_user_id:
            raise ForbiddenError("Forbidden: user cannot access this resource")

        results = self.table.query(
            KeyConditionExpression=Key("id").eq(self.USER_PREFIX + user_id)
        )
        if results["Count"] == 0:
            raise NotFoundError
        else:
            return results["Items"][0]

    def get_gigs_for_user(self, user_id: str, requesting_user_id: str):
        if user_id != requesting_user_id:
            raise ForbiddenError("Forbidden: user cannot access this resource")

        results = self.table.query(
            IndexName="userId-id-index",
            KeyConditionExpression=(
                Key("userId").eq(self.USER_PREFIX + user_id)
                & Key("id").begins_with(self.GIG_PREFIX)
            ),
        )
        return results["Items"]

    def get_gig_by_id(self, gig_id: str, requesting_user_id: str):
        results = self.table.query(
            KeyConditionExpression=Key("id").eq(self.GIG_PREFIX + gig_id)
        )
        if results["Count"] == 0:
            raise NotFoundError
        else:
            gig = results["Items"][0]
            if gig["userId"] != self.USER_PREFIX + requesting_user_id:
                raise ForbiddenError("Forbidden: user cannot access this resource")
            return results["Items"][0]

    def post_gig(self, gig: Gig, requesting_user_id: str):
        if gig.userId != self.USER_PREFIX + requesting_user_id:
            raise ForbiddenError("Forbidden: user cannot create gig for another user")
        item: dict = gig.model_dump()
        item["date"] = gig.date.strftime("%Y-%m-%d")
        item["id"] = self.GIG_PREFIX + str(gig.id)
        self.table.put_item(Item=item)
        return {"message": "Created gig with ID " + str(gig.id)}

    def delete_gig(self, gig_id: str, requesting_user_id: str):
        full_gig_id = self.GIG_PREFIX + gig_id
        results = self.table.query(KeyConditionExpression=Key("id").eq(full_gig_id))
        if results["Count"] == 0:
            raise NotFoundError
        else:
            user_id = results["Items"][0]["userId"]
            if user_id != self.USER_PREFIX + requesting_user_id:
                raise ForbiddenError("Forbidden: user cannot delete this resource")
            self.table.delete_item(Key={"id": full_gig_id, "userId": user_id})
            return {"message": f"Deleted gig with ID {gig_id}"}

    def post_integration(self, integration: Integration, requesting_user_id: str):
        user_id = integration.userId.split("#")[-1]
        if user_id != requesting_user_id:
            raise ForbiddenError("Forbidden: user cannot create integration for another user")

        user = self.get_user_by_id(user_id, requesting_user_id)
        existing_integrations = [exist_int["type"] for exist_int in user.get("integrations", [])]
        if integration.type in existing_integrations:
            raise ForbiddenError(f"Forbidden: user already has an integration of type {integration.type}")

        item: dict = integration.model_dump()
        item["id"] = self.INTEGRATION_PREFIX + str(integration.id)
        self.table.put_item(Item=item)

        self.table.update_item(
            Key={
                "id": integration.userId,
                "userId": integration.userId,
            },
            UpdateExpression="""
                SET integrations = list_append(
                    if_not_exists(integrations, :empty_list),
                    :new_item
                )
            """,
            ExpressionAttributeValues={
                ":empty_list": [],
                ":new_item": [
                    {
                        "type": integration.type,
                        "id": item["id"],
                    }
                ],
            },
        )
        return {"message": "Created integration with ID " + str(integration.id)}
