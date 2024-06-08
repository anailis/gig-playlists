import logging
from datetime import date

from boto3.dynamodb.conditions import Key

from spotify_playlist_client import SpotifyPlaylistClient
from gig import Gig
from upcoming_playlist_client import UpcomingPlaylistClient
from user import User


logger = logging.getLogger()


class UpcomingPlaylistReconService:
    def __init__(self, table, scheduler,
                 spotify_client: SpotifyPlaylistClient,
                 target_arn: str,
                 role_arn: str):
        self.table = table
        self.spotify_client = spotify_client
        self.upcoming_playlist_client = UpcomingPlaylistClient(
            spotify_client=spotify_client,
            table=table,
            scheduler=scheduler,
            target_arn=target_arn,
            role_arn=role_arn,
        )

    def reconcile_playlist(self, user_id: str) -> None:
        """
        Reconciles a user's upcoming gigs playlist against the gigs database.
        Artists in the playlist without upcoming gigs in the db are removed.
        Artists with upcoming gigs not in the playlist are added.

        Attributes:
            user_id (str): The user's Spotify ID.
        """
        user_details = self._get_user_details(user_id)
        upcoming_gigs = self._get_upcoming_gigs(user_id)
        artists_in_playlist = self.spotify_client.get_artists_in_playlist(
            user_details.upcomingPlaylistId
        )

        gigs_to_add = []
        artists_to_remove = artists_in_playlist
        for gig in upcoming_gigs:
            if gig.spotifyArtistId not in artists_in_playlist:
                gigs_to_add.append(gig)
            else:
                artists_to_remove.remove(gig.spotifyArtistId)

        for artist in artists_to_remove:
            self.spotify_client.remove_artist(artist, user_details.upcomingPlaylistId)
        logger.info(f"Removed {len(artists_to_remove)} artists from playlist")

        self.upcoming_playlist_client.process_gigs(
            gigs=gigs_to_add,
            user_details={user_id: user_details}
        )

    def _get_user_details(self, user_id: str) -> User:
        results = self.table.query(KeyConditionExpression=Key("id").eq(user_id))
        return User.construct(**results["Items"][0])

    def _get_upcoming_gigs(self, user_id: str) -> list[Gig]:
        results = self.table.query(
            IndexName="userId-date-index",
            KeyConditionExpression=(
                    Key("userId").eq(user_id)
                    & Key("date").gt(date.today().strftime("%Y-%m-%d"))
            )
        )["Items"]
        logger.info(f"Found {len(results)} upcoming gigs")
        return [Gig.construct(**gig) for gig in results]

