from typing import List, Optional

from genie_common.models.openai import EmbeddingsModel
from genie_common.clients.openai import OpenAIClient
from genie_common.tools import logger
from genie_datastores.milvus import MilvusClient
from genie_datastores.milvus.models import SearchRequest
from genie_datastores.milvus.utils import convert_iterable_to_milvus_filter
from spotipyio.logic.collectors.search_collectors.spotify_search_type import SpotifySearchType

from server.consts.api_consts import ID
from server.data.prompt_details import PromptDetails
from server.logic.database_client import DatabaseClient
from server.utils.spotify_utils import sample_uris, to_uris


class PromptDetailsTracksSelector:
    def __init__(self,
                 db_client: DatabaseClient,
                 openai_client: OpenAIClient,
                 milvus_client: MilvusClient):
        self._db_client = db_client
        self._openai_client = openai_client
        self._milvus_client = milvus_client

    async def select_tracks(self, prompt_details: PromptDetails) -> List[str]:
        tracks_ids = None

        if prompt_details.musical_parameters:
            tracks_ids = await self._db_client.query(prompt_details.musical_parameters)

        if prompt_details.textual_parameters and tracks_ids != []:
            logger.info("Filtering tracks by textual relevance")
            tracks_ids = await self._embed_and_search(prompt_details.textual_parameters, tracks_ids)

        return self._select_uris(tracks_ids)

    async def _embed_and_search(self, text: str, tracks_ids: Optional[List[str]]) -> List[str]:
        prompt_embeddings = await self._openai_client.embeddings.collect(text=text, model=EmbeddingsModel.ADA)

        if prompt_embeddings is None:
            logger.warn(f"Could not generate embeddings for textual parameters `{text}`. Returning original tracks ids")
            return tracks_ids

        return await self._search_embeddings_db_for_nearest_neighbors(prompt_embeddings, tracks_ids)

    async def _search_embeddings_db_for_nearest_neighbors(self,
                                                          prompt_embeddings: Optional[List[float]],
                                                          musical_tracks_ids: Optional[List[str]]) -> List[str]:
        request_filter = self._build_textual_search_filter(musical_tracks_ids)
        request = SearchRequest(
            collection_name="track_names_embeddings",
            vector=prompt_embeddings,
            filter=request_filter
        )
        response = await self._milvus_client.vectors.search(request)  # TODO: Integrate here distance threshold

        return [track[ID] for track in response]

    @staticmethod
    def _build_textual_search_filter(tracks_ids: Optional[List[str]]) -> Optional[str]:
        if tracks_ids is not None:
            return convert_iterable_to_milvus_filter(field_name=ID, iterable=tracks_ids)

    @staticmethod
    def _select_uris(tracks_ids: Optional[List[str]]) -> List[str]:
        if tracks_ids is None:
            return []

        uris = to_uris(SpotifySearchType.TRACK, *tracks_ids)
        uris_subset = sample_uris(uris)

        return sorted(uris_subset)
