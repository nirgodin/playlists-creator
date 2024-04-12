from functools import partial
from typing import List, Optional

from genie_common.tools import AioPoolExecutor, logger
from genie_common.utils import safe_nested_get
from spotipyio import SpotifyClient, SearchItemMetadata, SearchItemFilters, EntityMatcher, MatchingEntity
from spotipyio.logic.collectors.search_collectors.search_item import SearchItem
from spotipyio.logic.collectors.search_collectors.spotify_search_type import SpotifySearchType

from server.consts.api_consts import ID
from server.consts.data_consts import ARTISTS, ITEMS


class ArtistsSearcher:
    def __init__(self, pool_executor: AioPoolExecutor, entity_matcher: EntityMatcher):
        self._pool_executor = pool_executor
        self._entity_matcher = entity_matcher

    async def search(self, artists_names: List[str], spotify_client: SpotifyClient) -> List[str]:
        logger.info(f"Searching Spotify for {len(artists_names)} artists")
        return await self._pool_executor.run(
            iterable=artists_names,
            func=partial(self._search_single_artist, spotify_client),
            expected_type=str
        )

    async def _search_single_artist(self, spotify_client: SpotifyClient, artist: str) -> Optional[str]:
        search_item = SearchItem(
            filters=SearchItemFilters(
                artist=artist
            ),
            metadata=SearchItemMetadata(
                search_types=[SpotifySearchType.ARTIST],
            ),
        )
        response = await spotify_client.search.run_single(search_item)

        if not isinstance(response, dict):
            logger.warning(f"Received unexpected response type `{type(response)}` from Spotify. Returning None instead")
            return

        entity = MatchingEntity(artist=artist)
        is_matching, _ = self._entity_matcher.match(entity=entity, candidate=response)

        if is_matching:
            return self._extract_artist_id(response=response)

    @staticmethod
    def _extract_artist_id(response: dict) -> Optional[str]:
        items = safe_nested_get(response, [ARTISTS, ITEMS], default=[])

        if items:
            first_item = items[0]
            return first_item[ID]
