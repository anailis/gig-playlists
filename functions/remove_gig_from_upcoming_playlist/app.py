import base64
import logging
import os

import boto3
import spotipy
from spotipy import SpotifyOAuth
from aws_lambda_powertools.utilities.typing import LambdaContext

from gigs_db.gigs_db_service import GigsDbService, IntegrationType
from spotify.spotify_playlist_client import SpotifyPlaylistClient

ssm_client = boto3.client("ssm")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])
gigs_db_service = GigsDbService(table)
kms_client = boto3.client("kms")
logger = logging.getLogger()
logger.setLevel("INFO")


auth = SpotifyOAuth(
    client_id=ssm_client.get_parameter(Name="/spotify/client_id")["Parameter"]["Value"],
    client_secret=ssm_client.get_parameter(
        Name="/spotify/client_secret", WithDecryption=True
    )["Parameter"]["Value"],
    redirect_uri=os.environ["SPOTIFY_REDIRECT_URI"],
    scope=[
        "playlist-modify-public",
        "playlist-modify-private",
        "playlist-read-private",
        "playlist-read-collaborative",
    ],
)


def lambda_handler(event: dict[str, str], context: LambdaContext) -> dict:
    """
    Removes an artist from a playlist.

    Attributes:
        event (dict[str, str]): must contain keys spotifyArtistId and playlistId

    Returns:
        artist_added (bool): True if artist was removed, False otherwise.
    """
    try:
        artist_id = event["spotifyArtistId"]
    except KeyError:
        logger.error(
            "Payload to RemoveGigFromUpcomingPlaylist must supply spotifyArtistId"
        )
        raise

    try:
        playlist_id = event["playlistId"]
    except KeyError:
        logger.error("Payload to RemoveGigFromUpcomingPlaylist must supply playlistId")
        raise

    try:
        user_id = event["userId"]
    except KeyError:
        logger.error("Payload to RemoveGigFromUpcomingPlaylist must supply userId")
        raise

    integration = gigs_db_service.get_integration_for_user(IntegrationType.SPOTIFY, user_id, prefix_user_id=False)
    refresh_token = kms_client.decrypt(
        KeyId=os.environ["KEY_ID"],
        CiphertextBlob=base64.b64decode(integration["refreshToken"]),
    )["Plaintext"].decode("utf-8")
    response = auth.refresh_access_token(refresh_token)

    spotify = spotipy.Spotify(auth=response["access_token"])
    spotify_client = SpotifyPlaylistClient(
        spotify=spotify,
    )

    return {
        "spotifyArtistId": artist_id,
        "playlistId": playlist_id,
        "removed": spotify_client.remove_artist(artist_id, playlist_id),
    }
