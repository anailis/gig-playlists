from typing import Optional
from itertools import chain
from collections import Counter
import logging

import spotipy

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel("INFO")


class SpotifyPlaylistClient:
    MIN_TRACKS_PER_ARTIST = 10
    MAX_TRACKS_PER_ARTIST = 30

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
                and artists_in_playlist[artist_id] >= self.MIN_TRACKS_PER_ARTIST)

    def _find_track_uris_from_names(self, artist_name: str, track_names: set[str]) -> set[str]:
        track_uris = set()
        tracks_not_found = set()
        # TODO: fix special characters e.g. "I'm Scum"
        for track in track_names:
            results = self.sp.search(
                q=f'track:"{track}" artist:"{artist_name}"',
                type="track",
                limit=1,
            )

            if len(results["tracks"]["items"]) == 0:
                tracks_not_found.add(track)
            else:
                track_uris.add(results["tracks"]["items"][0]["uri"])
                if len(track_uris) == self.MAX_TRACKS_PER_ARTIST:
                    logger.info(f"Max tracks for artist ({self.MAX_TRACKS_PER_ARTIST}) reached")
                    break

        logger.info(f"{len(track_uris)} of {len(track_names)} tracks found")
        logger.info(f"Tracks not found: {tracks_not_found}")
        return track_uris

    def _find_all_tracks_by_artist_in_playlist(self, artist_id: str) -> list[str]:
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
                "upcoming gigs_db_crud",
                public=False,
                collaborative=False,
            )["id"]
            logger.info(f"Created playlist with ID {playlist}")
        else:
            playlist = self.playlist_id
            if self._artist_is_in_playlist(artist_id):
                logger.info(f"Playlist already contains artist {artist_id}")
                return

        tracks = self.sp.artist_top_tracks(artist_id)["tracks"]
        self.sp.playlist_add_items(
            playlist_id=playlist,
            items=[t["uri"] for t in tracks]
        )
        logger.info(
            f"Added {len(tracks)} tracks "
            f"by artist {artist_id} "
            f"to playlist {playlist}"
        )

    def remove_artist(self, artist_id: str) -> None:
        if self.playlist_id is None:
            return

        tracks_to_remove = self._find_all_tracks_by_artist_in_playlist(artist_id)
        if len(tracks_to_remove) > 0:
            logger.info(f"Removed {len(tracks_to_remove)} songs by artist {artist_id}")
            self.sp.playlist_remove_all_occurrences_of_items(
                playlist_id=self.playlist_id,
                items=tracks_to_remove
            )
        else:
            logger.info(f"Artist {artist_id} not in playlist")

    def add_tracks(self, artist_name: str, track_names: set[str]) -> None:
        track_uris = self._find_track_uris_from_names(
            artist_name=artist_name,
            track_names=track_names,
        )

        self.sp.playlist_add_items(
            playlist_id=self.playlist_id,
            items=track_uris
        )
