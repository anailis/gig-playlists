import json
from datetime import date, datetime, timedelta

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from aws_lambda_powertools.logging import Logger
from spotipy import SpotifyException

from spotify_playlist_client import SpotifyPlaylistClient

from gig import Gig
from user import User

logger = Logger()


class UpcomingPlaylistClient:
    def __init__(self, table, scheduler,
                 spotify_client: SpotifyPlaylistClient,
                 target_arn: str,
                 role_arn: str):
        self.table = table
        self.scheduler = scheduler
        self.spotify_client = spotify_client
        self.target_arn = target_arn
        self.role_arn = role_arn

    def process_gigs(self, gigs: list[Gig], user_details: dict[str, User] = None) -> dict[str: list[str]]:
        """
            Adds artists to an upcoming playlist based on a list of gigs.
            Schedules removal of artists from the playlist after the gig.
            Handles duplicates and irrelevant gigs (e.g. in the past).

            Attributes:
                gigs (list[Gig]): A list of Gigs to be added to the playlist.
                user_details (dict[str, User]): Dictionary relating user IDs to User objects.

            Returns:
                added (dict[str: list[str]): Dictionary mapping user IDs to
                  Spotify artist IDs added to upcoming playlist.
        """
        gigs_by_user = {}
        if user_details is None:
            user_details = {}
        else:
            for user in user_details.keys():
                gigs_by_user[user] = []

        for gig in gigs:
            # TODO: songs not guaranteed to be removed at latest date if multiple for one artist
            logger.info("Received gig", gig_id=gig.id)

            if gig.userId not in user_details.keys():
                user_details[gig.userId] = self._get_user_details(gig.userId)
                gigs_by_user[gig.userId] = []

            if gig.date <= date.today():
                logger.info("Gig occurred in the past; skipping", gig_id=gig.id)
                continue

            if gig.spotifyArtistId not in gigs_by_user[gig.userId]:
                playlist_id = user_details[gig.userId].upcomingPlaylistId
                try:
                    artist_added = self.spotify_client.add_artist(
                        gig.spotifyArtistId,
                        playlist_id
                    )
                except SpotifyException as err:
                    logger.warning(
                        f"Unable to add artist to playlist: {err}",
                        gig_id=gig.id,
                        artist_id=gig.spotifyArtistId
                    )
                    continue

                if artist_added:
                    try:
                        schedule = self._schedule_removal_of_artist(gig, playlist_id)
                        gigs_by_user[gig.userId].append(gig.spotifyArtistId)
                        logger.info("Created schedule", schedule_id=schedule)
                    except ClientError as err:
                        logger.warning(f"Unable to schedule delete for gig {gig.id}: {err}")
                        try:
                            self.spotify_client.remove_artist(
                                gig.spotifyArtistId,
                                playlist_id
                            )
                        except SpotifyException as err:
                            logger.warning(
                                f"Unable to remove artist from playlist: {err}",
                                gig_id=gig.id,
                                artist_id=gig.spotifyArtistId,
                                playlist_id=playlist_id
                            )
                            continue

        return gigs_by_user

    def _get_user_details(self, user_id: str) -> User:
        logger.info("Searching for user", user_id=user_id)
        results = self.table.query(KeyConditionExpression=Key("id").eq(user_id))
        try:
            return User.model_construct(**results["Items"][0])
        except IndexError:
            raise ValueError(f"No user with ID {user_id} exists")

    def _schedule_removal_of_artist(self, gig: Gig, playlist_id: str) -> str:
        delete_date = datetime.strftime(
            gig.date + timedelta(days=1),
            "%Y-%m-%dT%H:%M:%S"
        )
        schedule_name = f"delete_{gig.spotifyArtistId}_from_{playlist_id}"
        self.scheduler.create_schedule(
            Name=schedule_name,
            Description=f"Delete {gig.artist} from playlist {playlist_id}",
            ActionAfterCompletion="DELETE",
            ScheduleExpression=f"at({delete_date})",
            FlexibleTimeWindow={"Mode": "OFF"},
            Target={
                "Arn": self.target_arn,
                "RoleArn": self.role_arn,
                "Input": json.dumps({
                    "spotifyArtistId": gig.spotifyArtistId,
                    "playlistId": playlist_id
                })
            },
        )
        return schedule_name
