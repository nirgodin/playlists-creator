from functools import partial
from typing import List, Dict, Optional

from aiohttp import ClientSession
from asyncio_pool import AioPool
from tqdm import tqdm

from server.consts.api_consts import SEARCH_URL
from server.consts.data_consts import ARTIST, TYPE, QUERY, ARTISTS, ITEMS, ORIGINAL_INPUT
from server.logic.access_token_generator import AccessTokenGenerator
from server.utils.general_utils import build_spotify_client_credentials_headers


class ArtistsCollector:
    def __init__(self, session: ClientSession):
        self._session = session
        self._access_token_generator = AccessTokenGenerator(session)

    async def collect(self, artists_names: List[str]) -> List[dict]:
        pool = AioPool(5)
        headers = await build_spotify_client_credentials_headers(self._access_token_generator)

        with tqdm(total=len(artists_names)) as progress_bar:
            func = partial(self._get_single_artist, headers, progress_bar)
            results = await pool.map(fn=func, iterable=artists_names)

        return [result for result in results if isinstance(result, dict)]

    async def _get_single_artist(self,
                                 headers: dict,
                                 progress_bar: tqdm,
                                 artist: str) -> Dict[str, str]:
        progress_bar.update(1)
        params = {
            QUERY: artist,
            TYPE: [ARTIST]
        }

        async with self._session.get(url=SEARCH_URL, params=params, headers=headers) as raw_response:
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
