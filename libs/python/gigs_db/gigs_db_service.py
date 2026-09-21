from datetime import date, datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4

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
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    userId: str
    type: IntegrationType
    refreshToken: str
    scope: str


class GigsDbService:
    GIG_PREFIX = "GIG#"
    USER_PREFIX = "USER#"
    INTEGRATION_PREFIX = "INTEGRATION#"

    def __init__(self, table):
        self.table = table

    def get_user_by_id(self, user_id: str, prefix_user_id=True):
        user_id = self.USER_PREFIX + user_id if prefix_user_id else user_id
        results = self.table.query(
            KeyConditionExpression=Key("id").eq(user_id)
        )
        if results["Count"] == 0:
            return None
        else:
            return results["Items"][0]

    def get_gigs_for_user(self, user_id: str):
        results = self.table.query(
            IndexName="userId-id-index",
            KeyConditionExpression=(
                Key("userId").eq(self.USER_PREFIX + user_id)
                & Key("id").begins_with(self.GIG_PREFIX)
            ),
        )
        return results["Items"]

    def get_gig_by_id(self, gig_id: str):
        results = self.table.query(
            KeyConditionExpression=Key("id").eq(self.GIG_PREFIX + gig_id)
        )
        if results["Count"] == 0:
            return None
        else:
            return results["Items"][0]

    def post_gig(self, gig: Gig):
        item: dict = gig.model_dump()
        item["date"] = gig.date.strftime("%Y-%m-%d")
        item["id"] = self.GIG_PREFIX + str(gig.id)
        self.table.put_item(Item=item)
        return {"message": "Created gig with ID " + str(gig.id)}

    def delete_gig(self, gig_id: str, user_id: str):
        self.table.delete_item(Key={"id": gig_id, "userId": user_id})
        return {"message": f"Deleted gig with ID {gig_id}"}

    def get_integrations_for_user(self, user_id: str):
        user = self.get_user_by_id(user_id)
        integration_ids = [integration["id"] for integration in user.get("integrations", [])]

        results = []
        for integration_id in integration_ids:
            results.append(self.table.query(KeyConditionExpression=Key("id").eq(integration_id)))
        return results

    def post_integration(self, integration: Integration):
        user_id = integration.userId.split("#")[-1]
        user = self.get_user_by_id(user_id)
        existing_integrations = [exist_int["type"] for exist_int in user.get("integrations", [])]
        if integration.type in existing_integrations:
            raise ValueError(f"User already has an integration of type {integration.type}")

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

    def get_integration_for_user(self, integration_type: IntegrationType, user_id: str, prefix_user_id=True):
        user = self.get_user_by_id(user_id, prefix_user_id=prefix_user_id)
        if user is None:
            raise ValueError("User with ID " + user_id + " does not exist")
        integration_ids = [
            integration["id"] for integration in user.get("integrations", [])
            if integration["type"] == integration_type
        ]
        if len(integration_ids) == 0:
            raise ValueError("User does not have an integration of type " + integration_type)
        elif len(integration_ids) > 1:
            raise ValueError("User has multiple integrations of type " + integration_type)

        results = self.table.query(
            KeyConditionExpression=Key("id").eq(integration_ids[0])
        )
        if results["Count"] == 0:
            raise ValueError("Could not find integration " + integration_ids[0])
        else:
            return results["Items"][0]
