from datetime import date
import json

from aws_lambda_powertools.utilities.data_classes.dynamo_db_stream_event import TypeDeserializer
from aws_lambda_powertools.utilities.parser import BaseModel
from pydantic import validator


class Gig(BaseModel):
    id: str
    artist: str
    userId: str
    date: date
    spotifyArtistId: str

    @validator("id", "userId", "date", "spotifyArtistId",
               pre=True, allow_reuse=True)
    def decode(cls, values):
        return TypeDeserializer().deserialize(values)

    def to_string(self) -> str:
        return json.dumps(self.__dict__, indent=4)