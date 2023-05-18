from functools import partial
from typing import List, Dict, Optional

from aiohttp import ClientSession
from asyncio_pool import AioPool
from tqdm import tqdm

from server.consts.api_consts import SEARCH_URL
from server.consts.data_consts import ARTIST, TYPE, QUERY, ARTISTS, ITEMS, ORIGINAL_INPUT, TRACK
from server.logic.openai.track_details import TrackDetails
from server.utils import build_spotify_client_credentials_headers


class SpotifyTracksCollector:
    async def collect(self, tracks_details: List[TrackDetails]) -> List[dict]:
        pool = AioPool(5)
        headers = build_spotify_client_credentials_headers()

        with tqdm(total=len(tracks_details)) as progress_bar:
            async with ClientSession(headers=headers) as session:
                func = partial(self._get_single_track, session, progress_bar)

                results = await pool.map(fn=func, iterable=tracks_details)

        return [result for result in results if result is not None]

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

        return self._extract_track_uri(response)

    @staticmethod
    def _extract_track_uri(response: dict) -> Optional[str]:
        if not isinstance(response, dict):
            return

        items = response.get(ARTISTS, {}).get(ITEMS, [])
        if not items:
            return

        first_item = items[0]

        return first_item
