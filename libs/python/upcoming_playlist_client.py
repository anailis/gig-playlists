import json
import logging
from datetime import date, datetime, timedelta

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from spotipy import SpotifyException

from spotify_playlist_client import SpotifyPlaylistClient

from gig import Gig
from user import User

logger = logging.getLogger()


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

    def process_gigs(self, gigs: list[Gig], user_details: dict[str, User] = None) -> None:
        gigs_by_user = {}
        if user_details is None:
            user_details = {}
        else:
            for user in user_details.keys():
                gigs_by_user[user] = []

        for gig in gigs:
            # TODO: songs not guaranteed to be removed at latest date if multiple for one artist
            logger.info(f"Received gig {gig.id}")

            if gig.date <= date.today():
                logger.info(f"Gig {gig.id} occurred in the past; skipping")
                return

            if gig.userId not in user_details.keys():
                user_details[gig.userId] = self._get_user_details(gig.userId)
                gigs_by_user[gig.userId] = []

            if gig.spotifyArtistId not in gigs_by_user[gig.userId]:
                gigs_by_user[gig.userId].append(gig.spotifyArtistId)
                playlist_id = user_details[gig.userId].upcomingPlaylistId
                try:
                    artist_added = self.spotify_client.add_artist(
                        gig.spotifyArtistId,
                        playlist_id
                    )
                except SpotifyException as err:
                    logger.warning(f"Unable to add artist {gig.spotifyArtistId} to playlist: {err}")
                    continue

                if artist_added:
                    try:
                        schedule = self._schedule_removal_of_artist(gig, playlist_id)
                        logger.info(f"Created schedule {schedule}")
                    except ClientError as err:
                        logger.warning(f"Unable to schedule delete for gig {gig.id}: {err}")

    def _get_user_details(self, user_id: str) -> User:
        results = self.table.query(KeyConditionExpression=Key("id").eq(user_id))
        return User.construct(**results["Items"][0])

    def _schedule_removal_of_artist(self, gig: Gig, playlist_id: str) -> str:
        delete_date = datetime.strftime(
            gig.date + timedelta(days=1),
            "%Y-%m-%dT%H:%M:%S"
        )
        schedule_name = f"delete_{gig.spotifyArtistId}"
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
