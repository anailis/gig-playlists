from typing import Optional, List
from itertools import chain
from collections import Counter

import spotipy


class UpcomingPlaylistClient:
    TRACKS_PER_ARTIST = 10

    def __init__(
            self,
            spotify: spotipy.Spotify,
            playlist: Optional[str] = None
    ):
        self.sp = spotify
        self.user_id = spotify.me()["id"]
        self.playlist_id = playlist

    @staticmethod
    def _extract_artist_ids_for_track(track):
        return [artist["id"] for artist in track["artists"]]

    def _artist_is_in_playlist(self, artist_id: str) -> bool:
        items = self.sp.playlist_items(self.playlist_id)["items"]
        print(items)
        artists_in_playlist = Counter(
            chain.from_iterable([
                self._extract_artist_ids_for_track(item["track"])
                for item in items
            ])
        )
        return (artist_id in artists_in_playlist
                and artists_in_playlist[artist_id] >= self.TRACKS_PER_ARTIST)

    def _find_all_tracks_by_artist(self, artist_id: str) -> List[str]:
        items = self.sp.playlist_items(self.playlist_id)["items"]
        return [
            item["track"]["uri"]
            for item in items
            if artist_id in self._extract_artist_ids_for_track(item["track"])
        ]

    def add_artist(self, artist_id: str) -> None:
        if self.playlist_id is None:
            playlist = self.sp.user_playlist_create(
                self.user_id,
                "upcoming gigs",
                public=False,
                collaborative=False,
            )["id"]
            print(f"Created playlist with ID {playlist}")
        else:
            playlist = self.playlist_id
            if self._artist_is_in_playlist(artist_id):
                print(f"Playlist already contains artist {artist_id}")
                return

        tracks = self.sp.artist_top_tracks(artist_id)["tracks"]
        self.sp.playlist_add_items(
            playlist_id=playlist,
            items=[t["uri"] for t in tracks]
        )
        print(
            f"Added {len(tracks)} tracks "
            f"by artist {artist_id} "
            f"to playlist {playlist}"
        )

    def remove_artist(self, artist_id: str) -> None:
        if self.playlist_id is None:
            return

        tracks_to_remove = self._find_all_tracks_by_artist(artist_id)
        if len(tracks_to_remove) > 0:
            print(f"Removed {len(tracks_to_remove)} songs by artist {artist_id}")
            self.sp.playlist_remove_all_occurrences_of_items(
                playlist_id=self.playlist_id,
                items=tracks_to_remove
            )
        else:
            print(f"Artist {artist_id} not in playlist")
