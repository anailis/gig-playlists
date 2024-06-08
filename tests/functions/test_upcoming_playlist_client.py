from datetime import date
from unittest.mock import Mock, patch

import pytest

from functions.add_gig_to_upcoming_playlist.upcoming_playlist_client import UpcomingPlaylistClient
from gig import Gig


CURRENT_DATE = date(2024, 1, 1)


@pytest.fixture()
def spotify_client(monkeypatch):
    class SpotifyClient:
        @classmethod
        def __init__(cls, a, b):
            pass

        @classmethod
        def add_artist(cls, artist_id):
            return True

    monkeypatch.setattr(
        "functions.add_gig_to_upcoming_playlist.upcoming_playlist_client.SpotifyPlaylistClient",
        SpotifyClient
    )


@pytest.fixture(autouse=True)
def fixed_date(monkeypatch):
    class FixedDate:
        @classmethod
        def today(cls):
            return CURRENT_DATE

    monkeypatch.setattr(
        "functions.add_gig_to_upcoming_playlist.upcoming_playlist_client.date",
        FixedDate
    )


@pytest.fixture
def table():
    table = Mock()
    table.query.return_value = {"Items": [{
        "id": "USER#1234",
        "userId": "USER#1234",
        "displayName": "user",
        "upcomingPlaylistId": "PLAYLIST12345"
    }]}
    return table


@pytest.fixture()
def spotify():
    spotify = Mock()
    spotify.me.return_value = {"id": "SPOTIFY_USER_ID"}
    return spotify


def test_gig_is_in_past(spotify, table, spotify_client):
    gig = Gig.construct(**{
        "id": "GIG#1234",
        "userId": "USER#1234",
        "date": date(2024, 12, 12),
        "spotifyArtistId": "abc"
    })

    upcoming_client = UpcomingPlaylistClient(table, spotify)
    upcoming_client.process_gigs([gig])
