from functools import partial
from typing import List, Optional

from aiohttp import ClientSession
from asyncio_pool import AioPool
from tqdm import tqdm

from server.consts.api_consts import ARTIST_TOP_TRACKS_URL, MARKET
from server.consts.data_consts import TRACKS
from server.logic.access_token_generator import AccessTokenGenerator
from server.utils.general_utils import build_spotify_client_credentials_headers


class ArtistsTopTracksCollector:
    def __init__(self, session: ClientSession):
        self._session = session
        self._access_token_generator = AccessTokenGenerator(self._session)

    async def collect(self, artists_ids: List[str], country: str) -> List[List[dict]]:
        pool = AioPool(5)
        headers = await build_spotify_client_credentials_headers(self._access_token_generator)

        with tqdm(total=len(artists_ids)) as progress_bar:
            func = partial(self._get_single_artist_tracks, headers, progress_bar, country)
            results = await pool.map(fn=func, iterable=artists_ids)

        return [result for result in results if isinstance(result, list)]

    async def _get_single_artist_tracks(self,
                                        headers: dict,
                                        progress_bar: tqdm,
                                        country: str,
                                        artist_id: str) -> Optional[List[dict]]:
        progress_bar.update(1)
        url = ARTIST_TOP_TRACKS_URL.format(artist_id)
        params = {
            MARKET: country
        }

        async with self._session.get(url=url, params=params, headers=headers) as raw_response:
            response = await raw_response.json()

        return self._extract_top_tracks(response)

    @staticmethod
    def _extract_top_tracks(response: dict) -> Optional[List[dict]]:
        if not isinstance(response, dict):
            return

        return response.get(TRACKS, None)
