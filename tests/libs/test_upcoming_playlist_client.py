import json
from datetime import date
from unittest.mock import Mock, call

import pytest
from botocore.exceptions import ClientError
from spotipy import SpotifyException

from upcoming_playlist_client import UpcomingPlaylistClient
from gig import Gig


CURRENT_DATE = date(2024, 1, 1)
PLAYLIST_ID = "PLAYLIST12345"
NONEXISTENT_ARTIST_ID = "UNKNOWN"
ARTIST_ID = "ARTIST"
TARGET_ARN = "arn:target"
ROLE_ARN = "arn:role"


@pytest.fixture(autouse=True)
def fixed_date(monkeypatch):
    class FixedDate:
        @classmethod
        def today(cls):
            return CURRENT_DATE

    monkeypatch.setattr(
        "upcoming_playlist_client.date",
        FixedDate
    )


@pytest.fixture()
def table():
    table = Mock()
    table.query.return_value = {"Items": [{
        "id": "USER#1234",
        "userId": "USER#1234",
        "displayName": "user",
        "upcomingPlaylistId": PLAYLIST_ID
    }]}
    return table


@pytest.fixture()
def scheduler():
    scheduler = Mock()
    return scheduler


@pytest.fixture()
def spotify_client():
    spotify = Mock()
    spotify.add_artist.return_value = True
    return spotify


@pytest.fixture()
def gig():
    return Gig.construct(**{
        "id": "GIG#1",
        "userId": "USER#1234",
        "date": date(2024, 3, 12),
        "spotifyArtistId": ARTIST_ID,
        "artist": "artist"
    })


def test_gig_is_in_future(table, spotify_client, scheduler, gig):
    upcoming_client = UpcomingPlaylistClient(
        table,
        scheduler,
        spotify_client,
        TARGET_ARN,
        ROLE_ARN
    )
    upcoming_client.process_gigs([gig])

    spotify_client.add_artist.assert_called_once()
    spotify_client.add_artist.assert_called_with(ARTIST_ID, PLAYLIST_ID)
    scheduler.create_schedule.assert_called_once()
    scheduler.create_schedule.assert_called_with(
        Name=f"delete_{ARTIST_ID}",
        Description=f"Delete artist from playlist {PLAYLIST_ID}",
        ActionAfterCompletion="DELETE",
        ScheduleExpression="at(2024-03-13T00:00:00)",
        FlexibleTimeWindow={"Mode": "OFF"},
        Target={
            "Arn": TARGET_ARN,
            "RoleArn": ROLE_ARN,
            "Input": json.dumps({
                "spotifyArtistId": ARTIST_ID,
                "playlistId": PLAYLIST_ID
            })
        },
    )


def test_gig_is_in_past(table, spotify_client, scheduler):
    gig = Gig.construct(**{
        "id": "GIG#1",
        "userId": "USER#1234",
        "date": date(2023, 12, 12),
        "spotifyArtistId": ARTIST_ID,
        "artist": "artist"
    })

    upcoming_client = UpcomingPlaylistClient(
        table,
        scheduler,
        spotify_client,
        TARGET_ARN,
        ROLE_ARN
    )
    upcoming_client.process_gigs([gig])

    spotify_client.add_artist.assert_not_called()
    scheduler.create_schedule.assert_not_called()


def test_user_has_multiple_gigs_for_same_artist(table, scheduler, spotify_client, gig):
    second_gig = Gig.construct(**{
        "id": "GIG#2",
        "userId": "USER#1234",
        "date": date(2024, 12, 12),
        "spotifyArtistId": ARTIST_ID,
        "artist": "artist"
    })

    upcoming_client = UpcomingPlaylistClient(
        table,
        scheduler,
        spotify_client,
        TARGET_ARN,
        ROLE_ARN
    )
    upcoming_client.process_gigs([gig, second_gig])

    spotify_client.add_artist.assert_called_once()
    spotify_client.add_artist.assert_called_with(ARTIST_ID, PLAYLIST_ID)
    scheduler.create_schedule.assert_called_once()
    scheduler.create_schedule.assert_called_with(
        Name=f"delete_{ARTIST_ID}",
        Description=f"Delete artist from playlist {PLAYLIST_ID}",
        ActionAfterCompletion="DELETE",
        ScheduleExpression="at(2024-03-13T00:00:00)",
        FlexibleTimeWindow={"Mode": "OFF"},
        Target={
            "Arn": TARGET_ARN,
            "RoleArn": ROLE_ARN,
            "Input": json.dumps({
                "spotifyArtistId": ARTIST_ID,
                "playlistId": PLAYLIST_ID
            })
        },
    )


def test_tracks_cannot_be_retrieved(table, scheduler, gig):
    spotify_client = Mock()
    exception = SpotifyException(
        "404",
        "NOT FOUND",
        "not found"
    )
    spotify_client.add_artist.side_effect = [exception, lambda x: True]

    invalid_gig = Gig.construct(**{
        "id": "GIG#2",
        "userId": "USER#1234",
        "date": date(2024, 12, 12),
        "spotifyArtistId": NONEXISTENT_ARTIST_ID,
        "artist": "artist not on spotify"
    })

    upcoming_client = UpcomingPlaylistClient(
        table,
        scheduler,
        spotify_client,
        TARGET_ARN,
        ROLE_ARN
    )
    upcoming_client.process_gigs([invalid_gig, gig])

    spotify_client.add_artist.assert_has_calls([
        call(NONEXISTENT_ARTIST_ID, PLAYLIST_ID),
        call(ARTIST_ID, PLAYLIST_ID)
    ])
    scheduler.create_schedule.assert_called_once()
    scheduler.create_schedule.assert_called_with(
        Name=f"delete_{ARTIST_ID}",
        Description=f"Delete artist from playlist {PLAYLIST_ID}",
        ActionAfterCompletion="DELETE",
        ScheduleExpression="at(2024-03-13T00:00:00)",
        FlexibleTimeWindow={"Mode": "OFF"},
        Target={
            "Arn": TARGET_ARN,
            "RoleArn": ROLE_ARN,
            "Input": json.dumps({
                "spotifyArtistId": ARTIST_ID,
                "playlistId": PLAYLIST_ID
            })
        },
    )


def test_schedule_cannot_be_made(table, spotify_client, gig):
    scheduler = Mock()
    exception = ClientError(
        {
            "Error": {
                "Code": "XXX",
                "Message": "RESOURCE QUOTA EXCEEDED"
            }
        },
        "CREATE SCHEDULE"
    )
    scheduler.create_schedule.side_effect = [exception, lambda x: True]

    invalid_gig = Gig.construct(**{
        "id": "GIG#2",
        "userId": "USER#6789",
        "date": date(2024, 12, 12),
        "spotifyArtistId": ARTIST_ID,
        "artist": "problem with schedule"
    })

    upcoming_client = UpcomingPlaylistClient(
        table,
        scheduler,
        spotify_client,
        TARGET_ARN,
        ROLE_ARN
    )
    upcoming_client.process_gigs([invalid_gig, gig])

    spotify_client.add_artist.assert_has_calls([
        call(ARTIST_ID, PLAYLIST_ID),
        call(ARTIST_ID, PLAYLIST_ID)
    ])
    scheduler.create_schedule.assert_has_calls([
        call(
            Name=f"delete_{ARTIST_ID}",
            Description=f"Delete problem with schedule from playlist {PLAYLIST_ID}",
            ActionAfterCompletion="DELETE",
            ScheduleExpression="at(2024-12-13T00:00:00)",
            FlexibleTimeWindow={"Mode": "OFF"},
            Target={
                "Arn": TARGET_ARN,
                "RoleArn": ROLE_ARN,
                "Input": json.dumps({
                    "spotifyArtistId": ARTIST_ID,
                    "playlistId": PLAYLIST_ID
                })
            }
        ),
        call(
            Name=f"delete_{ARTIST_ID}",
            Description=f"Delete artist from playlist {PLAYLIST_ID}",
            ActionAfterCompletion="DELETE",
            ScheduleExpression="at(2024-03-13T00:00:00)",
            FlexibleTimeWindow={"Mode": "OFF"},
            Target={
                "Arn": TARGET_ARN,
                "RoleArn": ROLE_ARN,
                "Input": json.dumps({
                    "spotifyArtistId": ARTIST_ID,
                    "playlistId": PLAYLIST_ID
                })
            }
        ),
    ])
