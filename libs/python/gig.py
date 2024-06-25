from datetime import date

from aws_lambda_powertools.utilities.parser import BaseModel, validator
from boto3.dynamodb.types import TypeDeserializer


class Gig(BaseModel):
    id: str
    artist: str
    userId: str
    date: date
    spotifyArtistId: str

    @classmethod
    @validator("id", "artist", "userId", "date", "spotifyArtistId",
               pre=True, allow_reuse=True)
    def decode(cls, values):
        return TypeDeserializer().deserialize(values)
