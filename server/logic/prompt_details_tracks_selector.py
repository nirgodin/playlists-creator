from typing import List

import pandas as pd
from spotipyio.logic.collectors.search_collectors.spotify_search_type import SpotifySearchType

from server.consts.data_consts import URI
from server.consts.path_consts import TRACK_NAMES_EMBEDDINGS_PATH
from server.data.prompt_details import PromptDetails
from server.logic.database_client import DatabaseClient
from server.logic.openai.embeddings_tracks_selector import EmbeddingsTracksSelector
from server.utils.spotify_utils import sample_uris, to_uris


class PromptDetailsTracksSelector:
    def __init__(self,
                 embeddings_tracks_selector: EmbeddingsTracksSelector,
                 db_client: DatabaseClient):
        self._embeddings_tracks_selector = embeddings_tracks_selector
        self._db_client = db_client
        self._embeddings_database = pd.read_csv(TRACK_NAMES_EMBEDDINGS_PATH)  # TODO: Remove and use Milvus DB instead

    async def select_tracks(self, prompt_details: PromptDetails) -> List[str]:
        uris = []

        if prompt_details.musical_parameters:
            tracks_ids = await self._db_client.query(prompt_details.musical_parameters)
            uris = to_uris(SpotifySearchType.TRACK, *tracks_ids)

        if prompt_details.textual_parameters:
            return await self._sort_uris_by_textual_relevance(uris, prompt_details.textual_parameters)

        return sample_uris(uris)

    async def _sort_uris_by_textual_relevance(self, uris: List[str], text: str) -> List[str]:
        embeddings_data = self._embeddings_database[self._embeddings_database[URI].isin(uris)]
        if embeddings_data.empty:
            return sample_uris(uris)

        return await self._embeddings_tracks_selector.select_tracks(embeddings_data, text)
