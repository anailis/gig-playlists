import logging
from datetime import date

from boto3.dynamodb.conditions import Key

from spotify_playlist_client import SpotifyPlaylistClient

from gig import Gig
from user import User

logger = logging.getLogger()


class UpcomingPlaylistClient:
    def __init__(self, table, spotify_client: SpotifyPlaylistClient):
        self.table = table
        self.dummy_client = spotify_client
        self.user_details = {}
        self.gigs_by_user = {}

    def process_gigs(self, gigs: list[Gig]) -> None:
        for gig in gigs:
            # TODO: songs not guaranteed to be removed at latest date if multiple for one artist
            logger.info(f"Received gig {gig.id}")

            if gig.date <= date.today():
                logger.info(f"Gig {gig.id} occurred in the past; skipping")
                return

            if gig.userId not in self.user_details.keys():
                self.user_details[gig.userId] = self._get_user_details(gig.userId)
                self.gigs_by_user[gig.userId] = []

            if gig.spotifyArtistId not in self.gigs_by_user[gig.userId]:
                self.dummy_client.add_artist(
                    gig.spotifyArtistId,
                    self.user_details[gig.userId].upcomingPlaylistId
                )
                # TODO: schedule deletion

    def _get_user_details(self, user_id: str) -> User:
        results = self.table.query(KeyConditionExpression=Key("id").eq(user_id))
        return User.construct(**results["Items"][0])
