from datetime import date

from aws_lambda_powertools.utilities.parser import BaseModel
from boto3.dynamodb.types import TypeDeserializer
from pydantic import field_validator


class Gig(BaseModel):
    id: str
    artist: str
    userId: str
    date: date
    spotifyArtistId: str

    @classmethod
    @field_validator("id", "artist", "userId", "date", "spotifyArtistId")
    def decode(cls, values):
        return TypeDeserializer().deserialize(values)
