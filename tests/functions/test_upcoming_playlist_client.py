from datetime import date
from unittest.mock import Mock

import pytest
from spotipy import SpotifyException

from functions.add_gig_to_upcoming_playlist.upcoming_playlist_client import UpcomingPlaylistClient
from gig import Gig


CURRENT_DATE = date(2024, 1, 1)
PLAYLIST_ID = "PLAYLIST12345"
ARTIST_ID = "ARTIST"


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
        "upcomingPlaylistId": PLAYLIST_ID
    }]}
    return table


@pytest.fixture()
def spotify_client():
    spotify = Mock()
    #spotify.add_artist.return_value = True
    return spotify


def test_gig_is_in_future(table, spotify_client):
    gig = Gig.construct(**{
        "id": "GIG#1234",
        "userId": "USER#1234",
        "date": date(2024, 12, 12),
        "spotifyArtistId": ARTIST_ID
    })

    upcoming_client = UpcomingPlaylistClient(table, spotify_client)
    upcoming_client.process_gigs([gig])

    spotify_client.add_artist.assert_called_once()
    spotify_client.add_artist.assert_called_with(ARTIST_ID, PLAYLIST_ID)


def test_gig_is_in_past(table, spotify_client):
    gig = Gig.construct(**{
        "id": "GIG#1234",
        "userId": "USER#1234",
        "date": date(2023, 12, 12),
        "spotifyArtistId": ARTIST_ID
    })

    upcoming_client = UpcomingPlaylistClient(table, spotify_client)
    upcoming_client.process_gigs([gig])

    spotify_client.add_artist.assert_not_called()


def test_tracks_cannot_be_retrieved(table):
    client = Mock()
    client.add_artist.side_effect = raise_spotify_exception
    gig = Gig.construct(**{
        "id": "GIG#1234",
        "userId": "USER#1234",
        "date": date(2024, 12, 12),
        "spotifyArtistId": ARTIST_ID
    })

    upcoming_client = UpcomingPlaylistClient(table, client)
    upcoming_client.process_gigs([gig])

    client.add_artist.assert_called_once()
    client.add_artist.assert_called_with(ARTIST_ID, PLAYLIST_ID)


def raise_spotify_exception(artist, playlist_id):
    raise SpotifyException(
        "404",
        "NOT FOUND",
        f"{artist} not found"
    )
