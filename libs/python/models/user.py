from pydantic import BaseModel


class User(BaseModel):
    id: str
    userId: str
    upcomingPlaylistId: str
