from functools import partial
from typing import List, Dict, Optional

from genie_common.tools import AioPoolExecutor, logger
from genie_common.utils import safe_nested_get
from spotipyio import SpotifyClient, SearchItemMetadata, SearchItemFilters
from spotipyio.logic.collectors.search_collectors.search_item import SearchItem
from spotipyio.logic.collectors.search_collectors.spotify_search_type import SpotifySearchType

from server.consts.data_consts import ARTISTS, ITEMS, ORIGINAL_INPUT


class ArtistsSearcher:
    def __init__(self, pool_executor: AioPoolExecutor):
        self._pool_executor = pool_executor

    async def search(self, artists_names: List[str], spotify_client: SpotifyClient) -> List[dict]:
        logger.info(f"Searching Spotify for {len(artists_names)} artists")
        return await self._pool_executor.run(
            iterable=artists_names,
            func=partial(self._search_single_artist, spotify_client),
            expected_type=dict
        )

    async def _search_single_artist(self, spotify_client: SpotifyClient, artist: str) -> Dict[str, str]:
        search_item = SearchItem(
            filters=SearchItemFilters(
                artist=artist
            ),
            metadata=SearchItemMetadata(
                search_types=[SpotifySearchType.ARTIST],
            ),
        )
        response = await spotify_client.search.run_single(search_item)

        return self._extract_artist_details(original_input=artist, response=response)

    @staticmethod
    def _extract_artist_details(original_input: str, response: dict) -> Optional[dict]:
        if not isinstance(response, dict):
            logger.warning(f"Received unexpected response type `{type(response)}` from Spotify. Returning None instead")
            return

        items = safe_nested_get(response, [ARTISTS, ITEMS], default=[])
        if items:
            first_item = items[0]
            first_item[ORIGINAL_INPUT] = original_input

            return first_item
