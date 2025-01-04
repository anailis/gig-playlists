from unittest.mock import Mock
import json
import pytest

import spotipy
from spotipy import SpotifyException

from spotify_playlist_client import SpotifyPlaylistClient

TEST_DATA_DIR = "tests/resources/test_data"
USER_ID = "12345"
PLAYLIST_ID = "6789"
ARTIST_NOT_IN_PLAYLIST = "1HxXNvsraqrsgfmju1yKk8"
ARTIST_WITH_ONE_SONG = "32kCEAvtuFzIZA15zrhQDW"
ARTIST_WITH_TEN_SONGS = "6FBDaR13swtiWwGhX1WQsP"


@pytest.fixture
def playlist_contents():
    with open(f"{TEST_DATA_DIR}/playlist_contents/all.json", "r") as f:
        playlist_contents = json.load(f)
    return playlist_contents


@pytest.fixture
def sp(playlist_contents):
    sp = Mock(spotipy.Spotify)
    sp.me.return_value = {"id": USER_ID}
    sp.user_playlist_create.return_value = {"id": PLAYLIST_ID}
    sp.playlist_items.return_value = playlist_contents
    return sp


@pytest.fixture()
def sp_top_tracks(sp, artist_id):
    with open(f"{TEST_DATA_DIR}/top_tracks/{artist_id}.json", "r") as f:
        top_tracks = json.load(f)
    sp.artist_top_tracks.return_value = top_tracks
    return sp


@pytest.fixture()
def top_track_uris(artist_id):
    with open(f"{TEST_DATA_DIR}/top_tracks/uris/{artist_id}.json", "r") as f:
        top_track_uris = json.load(f)["tracks"]
    return top_track_uris


@pytest.fixture()
def tracks_in_playlist(artist_id):
    with open(f"{TEST_DATA_DIR}/playlist_contents/{artist_id}.json", "r") as f:
        tracks_in_playlist = json.load(f)["tracks"]
    return tracks_in_playlist


@pytest.mark.parametrize("artist_id", [ARTIST_NOT_IN_PLAYLIST, ARTIST_WITH_ONE_SONG])
def test_tracks_added_to_existing_playlist(artist_id, sp_top_tracks, top_track_uris):
    client = SpotifyPlaylistClient(sp_top_tracks)
    client.add_artist(artist_id, PLAYLIST_ID)
    sp_top_tracks.playlist_add_items.assert_called_with(
        playlist_id=PLAYLIST_ID,
        items=top_track_uris
    )
    sp_top_tracks.user_playlist_create.assert_not_called()


def test_artist_has_songs_in_playlist_above_threshold(sp):
    client = SpotifyPlaylistClient(sp)
    client.add_artist(ARTIST_WITH_TEN_SONGS, PLAYLIST_ID)
    sp.user_playlist_create.assert_not_called()
    sp.playlist_add_items.assert_not_called()


def test_artist_not_in_playlist(sp):
    client = SpotifyPlaylistClient(sp)
    client.remove_artist(ARTIST_NOT_IN_PLAYLIST, PLAYLIST_ID)
    sp.playlist_remove_all_occurrences_of_items.assert_not_called()


@pytest.mark.parametrize("artist_id", [ARTIST_WITH_TEN_SONGS, ARTIST_WITH_ONE_SONG])
def test_artist_in_playlist(artist_id, sp, tracks_in_playlist):
    client = SpotifyPlaylistClient(sp)
    client.remove_artist(artist_id, PLAYLIST_ID)
    sp.playlist_remove_all_occurrences_of_items.assert_called_with(
        playlist_id=PLAYLIST_ID,
        items=tracks_in_playlist
    )


def raise_spotify_exception(artist):
    raise SpotifyException(
        "404",
        "NOT FOUND",
        f"{artist} not found"
    )
