from functools import partial
from typing import List, Optional

from aiohttp import ClientSession
from asyncio_pool import AioPool
from tqdm import tqdm

from server.consts.api_consts import SEARCH_URL
from server.consts.data_consts import TYPE, QUERY, ITEMS, TRACK, TRACKS
from server.logic.openai.track_details import TrackDetails
from server.utils.general_utils import build_spotify_client_credentials_headers
from server.utils.spotify_utils import extract_tracks_from_response


class SpotifyTracksCollector:
    async def collect(self, tracks_details: List[TrackDetails]) -> List[dict]:
        pool = AioPool(5)
        headers = build_spotify_client_credentials_headers()

        with tqdm(total=len(tracks_details)) as progress_bar:
            async with ClientSession(headers=headers) as session:
                func = partial(self._get_single_track, session, progress_bar)

                results = await pool.map(fn=func, iterable=tracks_details)

        return [result for result in results if result is not None and isinstance(result, dict)]

    async def _get_single_track(self,
                                session: ClientSession,
                                progress_bar: tqdm,
                                track_details: TrackDetails) -> Optional[str]:
        progress_bar.update(1)
        params = {
            QUERY: track_details.query,
            TYPE: [TRACK]
        }

        async with session.get(url=SEARCH_URL, params=params) as raw_response:
            response = await raw_response.json()

        return self._extract_track(response)

    @staticmethod
    def _extract_track(response: dict) -> Optional[str]:
        if not isinstance(response, dict):
            return

        tracks = extract_tracks_from_response(response)
        if not tracks:
            return

        return tracks[0]
