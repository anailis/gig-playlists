import os

import boto3
import spotipy
from aws_lambda_powertools.utilities.typing import LambdaContext
from spotipy import SpotifyOAuth

from spotify_playlist_client import SpotifyPlaylistClient
from spotipy_ssm_credentials_cache import SSMCacheHandler
from upcoming_playlist_recon_service import UpcomingPlaylistReconService

ssm_client = boto3.client("ssm")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

auth = SpotifyOAuth(
    client_id=ssm_client.get_parameter(Name="/spotify/client_id")[
        "Parameter"
    ]["Value"],
    client_secret=ssm_client.get_parameter(
        Name="/spotify/client_secret", WithDecryption=True
    )["Parameter"]["Value"],
    redirect_uri=ssm_client.get_parameter(Name="/spotify/redirect_url")[
        "Parameter"
    ]["Value"],
    scope=[
        "playlist-modify-private",
        "playlist-read-private",
    ],
    cache_handler=SSMCacheHandler("/spotify/credcache"),
)
spotify = spotipy.Spotify(auth_manager=auth)
recon_service = UpcomingPlaylistReconService(
    spotify_client=SpotifyPlaylistClient(spotify),
    table=table
)


def lambda_handler(event: dict, context: LambdaContext):
    recon_service.reconcile_playlist("USER#e60d3adf-1bd5-4b5e-b71c-42582ed86bd6")
    return ""
