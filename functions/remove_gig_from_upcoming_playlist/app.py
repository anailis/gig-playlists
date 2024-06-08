import logging

import boto3
import spotipy
from spotipy import SpotifyOAuth
from aws_lambda_powertools.utilities.typing import LambdaContext

from spotipy_ssm_credentials_cache import SSMCacheHandler
from spotify_playlist_client import SpotifyPlaylistClient

ssm_client = boto3.client("ssm")
logger = logging.getLogger()
logger.setLevel("INFO")


def lambda_handler(event: dict, context: LambdaContext) -> str:
    try:
        artist_id = event["spotifyArtistId"]
    except KeyError:
        logger.error("Payload to RemoveGigFromUpcomingPlaylist must supply spotifyArtistId")
        raise

    try:
        playlist_id = event["playlistId"]
    except KeyError:
        logger.error("Payload to RemoveGigFromUpcomingPlaylist must supply playlistId")
        raise

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
    spotify_client = SpotifyPlaylistClient(
        spotify=spotipy.Spotify(auth_manager=auth),
        playlist=playlist_id,
    )

    artist_removed = spotify_client.remove_artist(artist_id)

    if artist_removed:
        return f"Artist with Spotify ID {artist_id} removed from playlist"
    else:
        return f"Artist with Spotify ID {artist_id} not in playlist"
