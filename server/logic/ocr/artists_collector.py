from functools import partial
from typing import List, Dict, Optional

from aiohttp import ClientSession
from asyncio_pool import AioPool
from tqdm import tqdm

from server.consts.api_consts import SEARCH_URL
from server.consts.data_consts import ARTIST, TYPE, QUERY, ARTISTS, ITEMS, ORIGINAL_INPUT
from server.utils import build_spotify_client_credentials_headers


class ArtistsCollector:
    async def collect(self, artists_names: List[str]) -> List[dict]:
        pool = AioPool(5)
        headers = build_spotify_client_credentials_headers()

        with tqdm(total=len(artists_names)) as progress_bar:
            async with ClientSession(headers=headers) as session:
                func = partial(self._get_single_artist, session, progress_bar)

                results = await pool.map(fn=func, iterable=artists_names)

        return [result for result in results if result is not None]

    async def _get_single_artist(self,
                                 session: ClientSession,
                                 progress_bar: tqdm,
                                 artist: str) -> Dict[str, str]:
        progress_bar.update(1)
        params = {
            QUERY: artist,
            TYPE: [ARTIST]
        }

        async with session.get(url=SEARCH_URL, params=params) as raw_response:
            response = await raw_response.json()

        return self._extract_artist_details(original_input=artist, response=response)

    @staticmethod
    def _extract_artist_details(original_input: str, response: dict) -> Optional[dict]:
        if not isinstance(response, dict):
            return

        items = response.get(ARTISTS, {}).get(ITEMS, [])
        if not items:
            return

        first_item = items[0]
        first_item[ORIGINAL_INPUT] = original_input

        return first_item
