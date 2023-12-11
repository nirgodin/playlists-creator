from typing import List, Optional, Callable, Dict

from genie_common.utils import safe_nested_get
from spotipyio import SpotifyClient

from server.consts.api_consts import ID, MAX_TRACKS_NUMBER_PER_REQUEST
from server.consts.data_consts import TRACK, ARTISTS, AUDIO_FEATURES, TRACKS, IMAGES, COVER_IMAGE_URL
from server.consts.openai_consts import URL
from server.logic.playlist_imitation.playlist_details import PlaylistDetails
from server.utils.spotify_utils import extract_tracks_from_response, sample_uris


class PlaylistDetailsCollector:
    async def collect_playlist(self, playlist_id: str, spotify_client: SpotifyClient) -> Optional[PlaylistDetails]:
        playlist = await spotify_client.playlists.info.collect_single(playlist_id)
        tracks = extract_tracks_from_response(playlist)
        tracks_sample = sample_uris(tracks, MAX_TRACKS_NUMBER_PER_REQUEST)
        tracks_data = await self._collect_tracks_data(tracks_sample, spotify_client)
        tracks_data[COVER_IMAGE_URL] = self._extract_playlist_image_url(playlist)

        return PlaylistDetails.from_dict(tracks_data)

    async def _collect_tracks_data(self, tracks: List[dict], spotify_client: SpotifyClient) -> Dict[str, List[dict]]:
        track_data = {}

        for name, fetch_fn in self._fetch_functions.items():
            result = await fetch_fn(tracks, spotify_client)
            track_data[name] = result

        return track_data

    @staticmethod
    async def _fetch_audio_features(tracks: List[dict], spotify_client: SpotifyClient) -> List[dict]:
        tracks_ids = [safe_nested_get(track, [TRACK, ID]) for track in tracks]
        return await spotify_client.audio_features.run(tracks_ids)

    async def _fetch_tracks_artists(self, tracks: List[dict], spotify_client: SpotifyClient) -> List[dict]:
        artists_ids = [self._extract_main_artist_id(track) for track in tracks]
        return await spotify_client.artists.info.run(artists_ids)

    @staticmethod
    async def _fetch_tracks_details(tracks: List[dict], spotify_client: SpotifyClient) -> List[dict]:
        raw_tracks_details = [track.get(TRACK) for track in tracks]
        return [track for track in raw_tracks_details if track is not None]

    @staticmethod
    def _extract_main_artist_id(track: dict) -> Optional[str]:
        artists = track.get(TRACK, {}).get(ARTISTS, [])
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
