from typing import List, Union, Optional, Callable, Dict

from aiohttp import ClientSession

from server.consts.api_consts import PLAYLIST_URL_FORMAT, ID, AUDIO_FEATURES_URL_FORMAT, \
    ARTIST_URL_FORMAT, MAX_TRACKS_NUMBER_PER_REQUEST
from server.consts.data_consts import TRACK, ARTISTS, AUDIO_FEATURES, TRACKS
from server.logic.spotify_tracks_collector import SpotifyTracksCollector
from server.utils.general_utils import build_spotify_client_credentials_headers, sample_list
from server.utils.spotify_utils import extract_tracks_from_response


class PlaylistDetailsCollector:
    def __init__(self, session: Optional[ClientSession] = None):
        self._tracks_collector = SpotifyTracksCollector()
        self._session = session

    async def collect_playlist(self, playlist_id: str) -> Optional[Dict[str, List[dict]]]:
        playlist = await self._collect(url_format=PLAYLIST_URL_FORMAT, spotify_id=playlist_id)

        if playlist is None:
            return

        tracks = extract_tracks_from_response(playlist)
        tracks_sample_indexes = sample_list(len(tracks), MAX_TRACKS_NUMBER_PER_REQUEST)
        tracks_sample = [tracks[i] for i in tracks_sample_indexes]

        return await self._collect_tracks_data(tracks_sample)

    async def _collect(self, url_format: str, spotify_id: str) -> Union[dict, list]:
        url = url_format.format(spotify_id)

        async with self._session.get(url) as raw_response:
            if raw_response.ok:
                return await raw_response.json()

    async def _collect_tracks_data(self, tracks: List[dict]):
        track_data = {}

        for name, fetch_fn in self._fetch_functions.items():
            result = await fetch_fn(tracks)
            track_data[name] = result

        return track_data

    async def _fetch_audio_features(self, tracks: List[dict]) -> List[dict]:
        tracks_ids = [self._extract_track_id(track) for track in tracks]
        joined_ids = ','.join([track_id for track_id in tracks_ids if track_id is not None])
        audio_features = await self._collect(AUDIO_FEATURES_URL_FORMAT, joined_ids)

        return audio_features[AUDIO_FEATURES]

    async def _fetch_tracks_artists(self, tracks: List[dict]) -> List[dict]:
        artists_ids = [self._extract_main_artist_id(track) for track in tracks]
        joined_ids = ','.join([artist_id for artist_id in artists_ids if artist_id is not None])
        artists = await self._collect(ARTIST_URL_FORMAT, joined_ids)

        return artists[ARTISTS]

    @staticmethod
    async def _fetch_tracks_details(tracks: List[dict]) -> List[dict]:
        raw_tracks_details = [track.get(TRACK) for track in tracks]
        return [track for track in raw_tracks_details if track is not None]

    @staticmethod
    def _extract_track_id(track: dict) -> Optional[str]:
        return track.get(TRACK, {}).get(ID)

    @staticmethod
    def _extract_main_artist_id(track: dict) -> Optional[str]:
        artists = track.get(TRACK, {}).get(ARTISTS, [])
        if not artists:
            return

        first_artist = artists[0]
        return first_artist.get(ID)

    @property
    def _fetch_functions(self) -> Dict[str, Callable]:
        return {
            TRACKS: self._fetch_tracks_details,
            ARTISTS: self._fetch_tracks_artists,
            AUDIO_FEATURES: self._fetch_audio_features
        }

    async def __aenter__(self) -> "PlaylistDetailsCollector":
        headers = build_spotify_client_credentials_headers()
        self._session = await ClientSession(headers=headers).__aenter__()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._session.__aexit__(exc_type, exc_val, exc_tb)
