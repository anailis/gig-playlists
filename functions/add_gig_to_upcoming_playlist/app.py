import logging
import os
from typing import Optional

import boto3
import spotipy
from aws_lambda_powertools.utilities.parser import event_parser, envelopes
from spotipy import SpotifyOAuth

from upcoming_playlist_client import UpcomingPlaylistClient
from gig import Gig
from spotipy_ssm_credentials_cache import SSMCacheHandler

ssm_client = boto3.client("ssm")
scheduler_client = boto3.client("scheduler")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])
logger = logging.getLogger()
logger.setLevel("INFO")

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
client = UpcomingPlaylistClient(
    sp=spotipy.Spotify(auth_manager=auth),
    table=table
)
# target_arn=os.environ["REMOVE_LAMBDA_ARN"],
# role_arn=os.environ["SCHEDULER_ROLE_ARN"],


@event_parser(model=Gig, envelope=envelopes.DynamoDBStreamEnvelope)
def lambda_handler(event: list[dict[str, Optional[Gig]]], context) -> str:
    gigs = [e["NewImage"] for e in event]
    print(gigs)
    client.process_gigs(gigs)
    return ""
