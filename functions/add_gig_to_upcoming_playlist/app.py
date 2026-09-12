import base64
import os

import boto3
import spotipy
from aws_lambda_powertools.logging import Logger
from spotipy import SpotifyOAuth


from aws_lambda_powertools.utilities.data_classes import (
    event_source,
    DynamoDBStreamEvent,
)
from aws_lambda_powertools.utilities.typing import LambdaContext

from gigs_db.gigs_db_service import GigsDbService, IntegrationType
from spotify.spotify_playlist_client import SpotifyPlaylistClient
from upcoming_playlist.upcoming_playlist_client import UpcomingPlaylistClient
from models.gig import Gig


ssm_client = boto3.client("ssm")
scheduler_client = boto3.client("scheduler")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])
gigs_db_service = GigsDbService(table)
kms_client = boto3.client("kms")
logger = Logger()

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


@logger.inject_lambda_context(log_event=True)
@event_source(data_class=DynamoDBStreamEvent)
def lambda_handler(event: DynamoDBStreamEvent, context: LambdaContext) -> str:
    gigs = [Gig(**record.dynamodb.new_image) for record in event.records]
    logger.info("Parsed gigs", gigs=gigs)
    user_ids = {gig.userId for gig in gigs}
    if len(user_ids) > 1:
        raise ValueError("Multiple user IDs found in the event")
    user_id = next(iter(user_ids))

    print("user_id", user_id)
    integration = gigs_db_service.get_integration_for_user(IntegrationType.SPOTIFY, user_id, prefix_user_id=False)
    refresh_token = kms_client.decrypt(
        KeyId=os.environ["KEY_ID"],
        CiphertextBlob=base64.b64decode(integration["refreshToken"]),
    )["Plaintext"]
    access_token = auth.refresh_access_token(refresh_token)

    spotify = spotipy.Spotify(auth=access_token)
    client = UpcomingPlaylistClient(
        table=table,
        scheduler=scheduler_client,
        spotify_client=SpotifyPlaylistClient(spotify),
        target_arn=os.environ["REMOVE_LAMBDA_ARN"],
        role_arn=os.environ["SCHEDULER_ROLE_ARN"],
    )

    return client.process_gigs(gigs)
