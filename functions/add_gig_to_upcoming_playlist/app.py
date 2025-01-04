import os

import boto3
import spotipy
from aws_lambda_powertools.logging import Logger
from spotipy import SpotifyOAuth


from aws_lambda_powertools.utilities.data_classes import event_source, DynamoDBStreamEvent
from aws_lambda_powertools.utilities.typing import LambdaContext


from spotify_playlist_client import SpotifyPlaylistClient
from upcoming_playlist_client import UpcomingPlaylistClient
from gig import Gig
from spotipy_ssm_credentials_cache import SSMCacheHandler

ssm_client = boto3.client("ssm")
scheduler_client = boto3.client("scheduler")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])
logger = Logger()

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
client = UpcomingPlaylistClient(
    table=table,
    scheduler=scheduler_client,
    spotify_client=SpotifyPlaylistClient(spotify),
    target_arn=os.environ["REMOVE_LAMBDA_ARN"],
    role_arn=os.environ["SCHEDULER_ROLE_ARN"],
)


@logger.inject_lambda_context(log_event=True)
@event_source(data_class=DynamoDBStreamEvent)
def lambda_handler(event: DynamoDBStreamEvent, context: LambdaContext) -> str:
    gigs = [
        Gig(**record.dynamodb.new_image)
        for record in event.records
    ]
    logger.info("Parsed gigs", gigs=gigs)
    return client.process_gigs(gigs)
