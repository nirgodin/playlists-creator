from random import uniform
from time import sleep
from typing import List, Any, Dict

from _pytest.fixtures import fixture
from aioresponses import aioresponses
from genie_common.clients.openai import OpenAIClient
from genie_common.clients.openai.openai_consts import DATA, EMBEDDING
from genie_common.models.openai import EmbeddingsModel
from genie_common.utils import random_alphanumeric_string, random_boolean
from genie_datastores.postgres.models import AudioFeatures, SpotifyTrack, RadioTrack
from genie_datastores.testing.postgres import postgres_session
from spotipyio.models import SpotifySearchType

from server.consts.api_consts import ID
from server.consts.data_consts import IN_OPERATOR
from server.data.prompt_details import PromptDetails
from server.data.query_condition import QueryCondition
from server.logic.database_client import DatabaseClient
from server.logic.prompt_details_tracks_selector import PromptDetailsTracksSelector
from server.utils.spotify_utils import to_uris
from tests.server.integration.test_records import TestRecords
from tests.server.integration.test_resources import TestResources

OPENAI_EMBEDDINGS_ENDPOINT = 'https://api.openai.com/v1/embeddings'


class TestPromptDetailsTracksSelector:
    @fixture(scope="class", autouse=True)
    async def set_up(self, records: TestRecords, resources: TestResources, embeddings_records: List[dict]) -> None:
        async with postgres_session(records.engine):
            await records.insert()
            await resources.milvus.vectors.insert(
                collection_name="track_names_embeddings",
                records=embeddings_records
            )
            sleep(2)

            yield

    async def test_select_tracks__no_musical_parameters_match__returns_empty_list(
            self,
            audio_features: List[AudioFeatures],
            tracks_selector: PromptDetailsTracksSelector,
            embeddings_responses: aioresponses
    ):
        prompt_details = self._given_unmet_musical_parameters(audio_features)

        actual = await tracks_selector.select_tracks(prompt_details)

        assert actual == []
        assert not embeddings_responses.requests

    async def test_select_tracks__both_textual_and_musical_parameters__returns_both_params_match(
            self,
            musical_parameters: List[QueryCondition],
            textual_parameters: str,
            tracks_selector: PromptDetailsTracksSelector,
            random_explicit: bool,
            expected_only_musical_parameters_uris: List[str],
            embeddings_responses: aioresponses
    ):
        prompt_details = PromptDetails(musical_parameters=musical_parameters, textual_parameters=textual_parameters)

        actual = await tracks_selector.select_tracks(prompt_details)

        assert actual == expected_only_musical_parameters_uris
        self._assert_expected_embeddings_request(embeddings_responses, textual_parameters)

    async def test_select_tracks__no_textual_parameters__returns_musical_tracks_match(
            self,
            musical_parameters: List[QueryCondition],
            tracks_selector: PromptDetailsTracksSelector,
            expected_only_musical_parameters_uris: List[str],
            embeddings_responses: aioresponses
    ):
        prompt_details = PromptDetails(musical_parameters=musical_parameters, textual_parameters=None)

        actual = await tracks_selector.select_tracks(prompt_details)

        assert actual == expected_only_musical_parameters_uris
        assert not embeddings_responses.requests

    async def test_select_tracks__no_musical_parameters__returns_textual_parameters_match(
            self,
            tracks_selector: PromptDetailsTracksSelector,
            embeddings_responses: aioresponses,
            textual_parameters: str,
            expected_textual_uris: List[str]
    ):
        prompt_details = PromptDetails(musical_parameters=None, textual_parameters=textual_parameters)

        actual = await tracks_selector.select_tracks(prompt_details)

        assert actual == expected_textual_uris
        self._assert_expected_embeddings_request(embeddings_responses, textual_parameters)

    @fixture(scope="class")
    def tracks_selector(self,
                        db_client: DatabaseClient,
                        openai_client: OpenAIClient,
                        resources: TestResources) -> PromptDetailsTracksSelector:
        return PromptDetailsTracksSelector(
            db_client=db_client,
            openai_client=openai_client,
            milvus_client=resources.milvus
        )

    @fixture(scope="function")
    def embeddings_responses(self, resources: TestResources) -> aioresponses:
        with aioresponses(passthrough=[resources.milvus_testkit.uri]) as embeddings_responses:
            embeddings_responses.post(
                url=OPENAI_EMBEDDINGS_ENDPOINT,
                payload={
                    DATA: [
                        {EMBEDDING: self._random_embedding()}
                    ]
                }
            )

            yield embeddings_responses

    @fixture(scope="class")
    def textual_parameters(self) -> str:
        return random_alphanumeric_string(min_length=1)

    @fixture(scope="class")
    def musical_parameters(self, random_explicit: bool) -> List[QueryCondition]:
        return [
            QueryCondition(
                column=SpotifyTrack.explicit.key,
                operator=IN_OPERATOR,
                value=[random_explicit]
            )
        ]

    @fixture(scope="class")
    def embeddings_records(self, spotify_tracks: List[SpotifyTrack], resources: TestResources) -> List[dict]:
        ids = [track.id for track in spotify_tracks]
        return [{ID: id_, "embeddings": self._random_embedding()} for id_ in ids]

    @fixture(scope="class")
    def expected_textual_uris(self, embeddings_records: List[Dict[str, Any]]) -> List[str]:
        ids = [record[ID] for record in embeddings_records]
        uris = to_uris(SpotifySearchType.TRACK, *ids)

        return sorted(uris)

    @fixture(scope="class")
    def random_explicit(self) -> bool:
        return random_boolean()

    @fixture(scope="class")
    def expected_only_musical_parameters_uris(self,
                                              random_explicit: bool,
                                              radio_tracks: List[RadioTrack],
                                              spotify_tracks: List[SpotifyTrack]) -> List[str]:
        radio_tracks_ids = {track.track_id for track in radio_tracks}
        relevant_spotify_tracks = [track for track in spotify_tracks if track.id in radio_tracks_ids]
        matching_tracks_ids = [track.id for track in relevant_spotify_tracks if track.explicit is random_explicit]
        uris = to_uris(SpotifySearchType.TRACK, *matching_tracks_ids)

        return sorted(uris)

    @staticmethod
    def _given_unmet_musical_parameters(audio_features: List[AudioFeatures]) -> PromptDetails:
        max_valence = max([track.valence for track in audio_features])
        unmet_condition = QueryCondition(
            column=AudioFeatures.valence.key,
            operator=">=",
            value=max_valence + 1
        )

        return PromptDetails(
            musical_parameters=[unmet_condition],
            textual_parameters=random_alphanumeric_string()
        )

    @staticmethod
    def _random_embedding() -> List[float]:
        return [uniform(-1, 1) for _ in range(1536)]

    @staticmethod
    def _assert_expected_embeddings_request(embeddings_responses: aioresponses, textual_parameters: str) -> None:
        embeddings_responses.assert_called_once_with(
            url=OPENAI_EMBEDDINGS_ENDPOINT,
            method="POST",
            json={
                "input": textual_parameters,
                "model": EmbeddingsModel.ADA.value
            }
        )
