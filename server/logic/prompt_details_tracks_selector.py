from typing import List

from genie_common.models.openai import EmbeddingsModel
from genie_common.openai import OpenAIClient
from genie_common.tools import logger
from genie_datastores.milvus import MilvusClient
from genie_datastores.milvus.models import SearchRequest
from genie_datastores.milvus.utils import convert_iterable_to_milvus_filter
from spotipyio.logic.collectors.search_collectors.spotify_search_type import SpotifySearchType

from server.consts.api_consts import ID
from server.data.case_status import CaseStatus
from server.data.prompt_details import PromptDetails
from server.logic.database_client import DatabaseClient
from server.tools.case_progress_reporter import CaseProgressReporter
from server.utils.spotify_utils import sample_uris, to_uris


class PromptDetailsTracksSelector:
    def __init__(self,
                 db_client: DatabaseClient,
                 openai_client: OpenAIClient,
                 milvus_client: MilvusClient,
                 case_progress_reporter: CaseProgressReporter):
        self._db_client = db_client
        self._openai_client = openai_client
        self._milvus_client = milvus_client
        self._case_progress_reporter = case_progress_reporter

    async def select_tracks(self, case_id: str, prompt_details: PromptDetails) -> List[str]:
        tracks_ids = []

        if prompt_details.musical_parameters:
            async with self._case_progress_reporter.report(case_id=case_id, status=CaseStatus.TRACKS):
                tracks_ids = await self._db_client.query(prompt_details.musical_parameters)

        if prompt_details.textual_parameters:
            tracks_ids = await self._filter_tracks_by_textual_relevance(
                case_id=case_id,
                tracks_ids=tracks_ids,
                text=prompt_details.textual_parameters
            )

        uris = to_uris(SpotifySearchType.TRACK, *tracks_ids)
        return sample_uris(uris)

    async def _filter_tracks_by_textual_relevance(self, case_id: str, tracks_ids: List[str], text: str) -> List[str]:
        logger.info("Filtering tracks by textual relevance")

        async with self._case_progress_reporter.report(case_id=case_id, status=CaseStatus.TEXTUAL_QUERY):
            return await self._embed_and_search(text, tracks_ids)

    async def _embed_and_search(self, text: str, tracks_ids: List[str]) -> List[str]:
        prompt_embeddings = await self._openai_client.embeddings.collect(text=text, model=EmbeddingsModel.ADA)

        if prompt_embeddings is None:
            logger.warn(f"Could not generate embeddings for textual parameters `{text}`. Returning original tracks ids")
            return tracks_ids

        return await self._search_embeddings_db_for_nearest_neighbors(prompt_embeddings, tracks_ids)

    async def _search_embeddings_db_for_nearest_neighbors(self,
                                                          prompt_embeddings: List[float],
                                                          musical_tracks_ids: List[str]) -> List[str]:
        request_filter = convert_iterable_to_milvus_filter(field_name=ID, iterable=musical_tracks_ids)
        request = SearchRequest(
            collection_name="track_names_embeddings",
            vector=prompt_embeddings,
            filter=request_filter
        )
        response = await self._milvus_client.search(request)  # TODO: Integrate here distance threshold

        return [track[ID] for track in response["data"]]
