from datetime import date
from unittest.mock import Mock

import pytest

from functions.upcoming_playlist_recon.upcoming_playlist_recon_service import UpcomingPlaylistReconService


CURRENT_DATE = date(2024, 1, 1)
PLAYLIST_ID = "PLAYLIST12345"
USER_ID = "USER#1234"
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
    user = {"Items": [{
        "id": "USER#1234",
        "userId": "USER#1234",
        "displayName": "user",
        "upcomingPlaylistId": PLAYLIST_ID
    }]}
    gigs = {"Items": [
        {
            "id": "GIG#1",
            "userId": USER_ID,
            "date": date(2024, 8, 12),
            "spotifyArtistId": "1",
            "artist": "artist1"
        },
        {
            "id": "GIG#2",
            "userId": USER_ID,
            "date": date(2024, 3, 12),
            "spotifyArtistId": "2",
            "artist": "artist2"
        }
    ]}
    table.query.side_effect = [user, gigs]
    return table


@pytest.fixture()
def scheduler():
    scheduler = Mock()
    return scheduler


@pytest.fixture()
def spotify_client():
    spotify = Mock()
    spotify.add_artist.return_value = True
    spotify.get_artists_in_playlist.return_value = ["1", "3"]
    return spotify


def test_successful_recon(table, scheduler, spotify_client):
    recon_service = UpcomingPlaylistReconService(
        table,
        scheduler,
        spotify_client,
        TARGET_ARN,
        ROLE_ARN
    )
    recon_service.reconcile_playlist(USER_ID)

    spotify_client.remove_artist.assert_called_once()
    spotify_client.remove_artist.assert_called_with("3", PLAYLIST_ID)
    spotify_client.add_artist.assert_called_once()
    spotify_client.add_artist.assert_called_with("2", PLAYLIST_ID)
