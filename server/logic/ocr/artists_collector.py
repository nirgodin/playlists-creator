from functools import partial
from typing import List, Dict, Optional

from aiohttp import ClientSession
from asyncio_pool import AioPool
from tqdm import tqdm

from server.utils import build_spotify_client_credentials_headers

SEARCH_URL = 'https://api.spotify.com/v1/search'


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
            'q': artist,
            'type': ['artist']
        }

        async with session.get(url=SEARCH_URL, params=params) as raw_response:
            response = await raw_response.json()

        return self._extract_artist_details(original_input=artist, response=response)

    @staticmethod
    def _extract_artist_details(original_input: str, response: list) -> Optional[dict]:
        if not isinstance(response, dict):
            return

        items = response.get('artists', {}).get('items', [])
        if not items:
            return

        first_item = items[0]
        first_item['original_input'] = original_input

        return first_item
