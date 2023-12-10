from functools import partial
from typing import List, Dict, Optional

from genie_common.tools import AioPoolExecutor
from genie_common.utils import safe_nested_get
from spotipyio import SpotifyClient
from spotipyio.logic.collectors.search_collectors.search_item import SearchItem
from spotipyio.logic.collectors.search_collectors.spotify_search_type import SpotifySearchType

from server.consts.data_consts import ARTISTS, ITEMS, ORIGINAL_INPUT


class ArtistsCollector:
    def __init__(self, pool_executor: AioPoolExecutor):
        self._pool_executor = pool_executor

    async def collect(self, artists_names: List[str], spotify_client: SpotifyClient) -> List[dict]:
        return await self._pool_executor.run(
            iterable=artists_names,
            func=partial(self._get_single_artist, spotify_client),
            expected_type=dict
        )

    async def _get_single_artist(self, spotify_client: SpotifyClient, artist: str) -> Dict[str, str]:
        search_item = SearchItem(
            search_types=[SpotifySearchType.ARTIST],
            artist=artist
        )
        response = await spotify_client.search.collect_single(search_item)

        return self._extract_artist_details(original_input=artist, response=response)

    @staticmethod
    def _extract_artist_details(original_input: str, response: dict) -> Optional[dict]:
        if not isinstance(response, dict):
            return

        items = safe_nested_get(response, [ARTISTS, ITEMS], default=[])
        if items:
            first_item = items[0]
            first_item[ORIGINAL_INPUT] = original_input

            return first_item
