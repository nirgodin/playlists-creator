from typing import List, Optional, Callable, Dict

from spotipyio import SpotifyClient

from server.consts.api_consts import ID, MAX_TRACKS_NUMBER_PER_REQUEST
from server.consts.data_consts import ARTISTS, AUDIO_FEATURES, TRACKS, IMAGES
from server.consts.openai_consts import URL
from server.data.playlist_imitation.playlist_details import PlaylistDetails
from server.tools.case_progress_reporter import CaseProgressReporter
from server.utils.spotify_utils import sample_uris


class PlaylistDetailsCollector:
    def __init__(self, case_progress_reporter: CaseProgressReporter):
        self._case_progress_reporter = case_progress_reporter

    async def collect_playlist(self,
                               case_id: str,
                               tracks: List[dict],
                               spotify_client: SpotifyClient) -> Optional[PlaylistDetails]:
        async with self._case_progress_reporter.report(case_id=case_id, status="playlist_details"):
            tracks_sample = sample_uris(tracks, MAX_TRACKS_NUMBER_PER_REQUEST)
            tracks_data = await self._collect_tracks_data(tracks_sample, spotify_client)
            # tracks_data[COVER_IMAGE_URL] = self._extract_playlist_image_url(playlist)  # TODO: Think how to integrate

            return PlaylistDetails.from_dict(tracks_data)

    async def _collect_tracks_data(self, tracks: List[dict], spotify_client: SpotifyClient) -> Dict[str, List[dict]]:
        track_data = {}

        for name, fetch_fn in self._fetch_functions.items():
            result = await fetch_fn(tracks, spotify_client)
            track_data[name] = result

        return track_data

    @staticmethod
    async def _fetch_audio_features(tracks: List[dict], spotify_client: SpotifyClient) -> List[dict]:
        tracks_ids = [track.get(ID) for track in tracks if track.get(ID) is not None]
        return await spotify_client.audio_features.run(tracks_ids)

    async def _fetch_tracks_artists(self, tracks: List[dict], spotify_client: SpotifyClient) -> List[dict]:
        artists_ids = [self._extract_main_artist_id(track) for track in tracks]
        return await spotify_client.artists.info.run(artists_ids)

    @staticmethod
    async def _fetch_tracks_details(tracks: List[dict], spotify_client: SpotifyClient) -> List[dict]:
        return [track for track in tracks if track is not None]

    @staticmethod
    def _extract_main_artist_id(track: dict) -> Optional[str]:
        artists = track.get(ARTISTS, [])
        if not artists:
            return

        first_artist = artists[0]
        return first_artist.get(ID)

    @staticmethod
    def _extract_playlist_image_url(playlist: dict) -> Optional[str]:
        images = playlist.get(IMAGES, [])

        if images:
            first_image = images[0]
            return first_image.get(URL)

    @property
    def _fetch_functions(self) -> Dict[str, Callable]:
        return {
            TRACKS: self._fetch_tracks_details,
            ARTISTS: self._fetch_tracks_artists,
            AUDIO_FEATURES: self._fetch_audio_features
        }
