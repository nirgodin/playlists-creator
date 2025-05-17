from functools import partial
from typing import List, Optional

from genie_common.tools import AioPoolExecutor
from spotipyio import SpotifyClient

from server.consts.api_consts import ID, MAX_TRACKS_NUMBER_PER_REQUEST
from server.consts.data_consts import ARTISTS
from server.data.track_features import TrackFeatures
from server.utils.spotify_utils import sample_uris


class PlaylistDetailsCollector:
    def __init__(self, pool_executor: AioPoolExecutor):
        self._pool_executor = pool_executor

    async def collect(self,
                      tracks: List[dict],
                      spotify_client: SpotifyClient) -> Optional[List[TrackFeatures]]:
        if tracks:
            tracks_sample = sample_uris(tracks, MAX_TRACKS_NUMBER_PER_REQUEST)

            return await self._pool_executor.run(
                iterable=tracks_sample,
                func=partial(self._collect_tracks_data, spotify_client),
                expected_type=TrackFeatures
            )

    async def _collect_tracks_data(self, spotify_client: SpotifyClient, track: dict) -> Optional[TrackFeatures]:
        artist = await self._fetch_artist_features(track, spotify_client)
        audio = await self._fetch_audio_features(track, spotify_client)

        if artist and audio:
            return TrackFeatures(
                track=track,
                artist=artist,
                audio=audio
            )

    async def _fetch_artist_features(self, track: dict, spotify_client: SpotifyClient) -> Optional[dict]:
        artist_id = self._extract_main_artist_id(track)

        if artist_id is not None:
            artists = await spotify_client.artists.info.run([artist_id])

            if artists:
                return artists[0]

    @staticmethod
    def _extract_main_artist_id(track: dict) -> Optional[str]:
        artists = track.get(ARTISTS, [])
        if not artists:
            return

        first_artist = artists[0]
        return first_artist.get(ID)

    @staticmethod
    async def _fetch_audio_features(track: dict, spotify_client: SpotifyClient) -> Optional[dict]:
        track_id = track.get(ID)

        if track_id is not None:
            audio_features = await spotify_client.tracks.audio_features.run([track_id])

            if audio_features:
                return audio_features[0]
