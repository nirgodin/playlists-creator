from random import randint, choice
from typing import List, Dict, Union
from unittest.mock import AsyncMock

from _pytest.fixtures import fixture
from aioresponses import aioresponses
from genie_common.utils import random_alphanumeric_string, random_string_array
from genie_datastores.postgres.models import PlaylistEndpoint, CaseProgress, Case
from genie_datastores.postgres.operations import execute_query
from sqlalchemy import select

from server.consts.app_consts import PLAYLIST_DETAILS, PROMPT
from server.consts.data_consts import URI
from server.controllers.content_controllers.prompt_controller import PromptController
from server.data.case_status import CaseStatus
from server.data.playlist_creation_context import PlaylistCreationContext
from server.data.prompt_details import PromptDetails
from server.data.query_condition import QueryCondition
from server.data.track_details import TrackDetails
from server.logic.prompt.prompt_serialization_manager import PromptSerializationManager
from server.logic.prompt_details_tracks_selector import PromptDetailsTracksSelector
from tests.server.integration.controllers.playlist_controllers.base_playlist_controller_test import \
    BasePlaylistControllerTest
from tests.server.integration.controllers.playlist_controllers.playlist_controller_test_context import \
    PlaylistControllerTestContext
from tests.server.utils import build_spotify_url, \
    some_tracks_uris


class TestPromptController(BasePlaylistControllerTest):
    async def test_post__query_prompt(self,
                                      test_context: PlaylistControllerTestContext,
                                      serialization_manager: AsyncMock,
                                      prompt_details: PromptDetails,
                                      tracks_selector: AsyncMock):
        serialization_manager.serialize.return_value = prompt_details

        response = self._request(test_context)

        tracks_selector.select_tracks.assert_called_once_with(prompt_details)
        await self._assert_expected_base_controller_logic(response, test_context)
        self._assert_no_search_request_sent(test_context.mock_responses)

    async def test_post__track_details_prompt(self,
                                              test_context: PlaylistControllerTestContext,
                                              serialization_manager: AsyncMock,
                                              tracks_details: List[TrackDetails],
                                              tracks_selector: AsyncMock):
        serialization_manager.serialize.return_value = tracks_details

        response = self._request(test_context)

        tracks_selector.select_tracks.assert_not_called()
        await self._assert_expected_base_controller_logic(response, test_context)

    async def test_post__non_serializable_prompt__doesnt_create_playlist(self,
                                                                         test_context: PlaylistControllerTestContext,
                                                                         serialization_manager: AsyncMock,
                                                                         tracks_details: List[TrackDetails],
                                                                         tracks_selector: AsyncMock):
        serialization_manager.serialize.return_value = None

        response = self._request(test_context)

        self._assert_expected_response(response, test_context.case_id)
        tracks_selector.select_tracks.assert_not_called()
        self._assert_no_search_request_sent(test_context.mock_responses)
        await self._assert_case_completed(test_context)
        await self._assert_case_has_no_playlist_id(test_context)

    @fixture(scope="function")
    def controller(self,
                   context: PlaylistCreationContext,
                   serialization_manager: AsyncMock,
                   tracks_selector: AsyncMock) -> PromptController:
        return PromptController(
            context=context,
            serialization_manager=serialization_manager,
            prompt_details_tracks_selector=tracks_selector
        )

    @fixture(scope="class")
    def serialization_manager(self) -> AsyncMock:
        return AsyncMock(PromptSerializationManager)

    @fixture(scope="function")
    def tracks_selector(self, uris: List[str]) -> AsyncMock:
        mock_tracks_selector = AsyncMock(PromptDetailsTracksSelector)
        mock_tracks_selector.select_tracks.return_value = uris

        return mock_tracks_selector

    @fixture(scope="class")
    def prompt_details(self) -> PromptDetails:
        n_parameters = randint(0, 10)
        return PromptDetails(
            musical_parameters=[self._random_query_condition() for _ in range(n_parameters)],
            textual_parameters=random_alphanumeric_string()
        )

    @fixture(scope="class")
    def endpoint(self) -> PlaylistEndpoint:
        return PlaylistEndpoint.PROMPT

    @fixture(scope="class")
    def prompt(self) -> str:
        return random_alphanumeric_string()

    @fixture(scope="function")
    def payload(self, prompt: str) -> Dict[str, Union[bytes, str, dict]]:
        payload = self._get_basic_request_payload()
        payload[PLAYLIST_DETAILS][PROMPT] = prompt

        return payload

    @fixture(scope="class")
    def expected_progress_statuses(self) -> List[CaseStatus]:
        return [
            CaseStatus.CREATED,
            CaseStatus.PROMPT,
            CaseStatus.TRACKS,
            CaseStatus.PLAYLIST,
            CaseStatus.COVER,
            CaseStatus.COMPLETED,
        ]

    @fixture(scope="class")
    def uris(self) -> List[str]:
        return some_tracks_uris()

    @fixture(scope="function")
    def tracks_details(self, uris: List[str], mock_responses: aioresponses) -> List[TrackDetails]:
        tracks_details = []

        for uri in uris:
            details = TrackDetails(
                track_name=random_alphanumeric_string(),
                artist_name=random_alphanumeric_string()
            )
            tracks_details.append(details)
            self._set_single_track_details_response(mock_responses, details, uri)

        yield tracks_details

    @staticmethod
    def _random_query_condition() -> QueryCondition:
        operator = choice(["in", ">=", "<="])
        value = random_string_array() if operator == "in" else randint(0, 100)

        return QueryCondition(
            column=random_alphanumeric_string(),
            operator=operator,
            value=value
        )

    @staticmethod
    def _assert_no_search_request_sent(mock_responses: aioresponses) -> None:
        requests_paths = [url.raw_path for _, url in mock_responses.requests.keys()]
        assert not any(path.__contains__("search") for path in requests_paths)

    @staticmethod
    def _set_single_track_details_response(mock_responses: aioresponses, track_details: TrackDetails, uri: str) -> None:
        params = track_details.to_search_item().to_query_params()
        url = build_spotify_url(routes=["search"], params=params)

        mock_responses.get(
            url=url,
            payload={URI: uri}
        )

    @staticmethod
    async def _assert_case_completed(test_context: PlaylistControllerTestContext) -> None:
        query = (
            select(CaseProgress.status).
            where(CaseProgress.case_id == test_context.case_id)
            .order_by(CaseProgress.creation_date.desc())
            .limit(1)
        )
        query_result = await execute_query(engine=test_context.resources.engine, query=query)

        case_status = query_result.scalars().first()

        assert case_status == CaseStatus.COMPLETED.value

    @staticmethod
    async def _assert_case_has_no_playlist_id(test_context: PlaylistControllerTestContext) -> None:
        query = (
            select(Case.playlist_id).
            where(Case.id == test_context.case_id)
        )
        query_result = await execute_query(engine=test_context.resources.engine, query=query)

        playlist_id = query_result.scalars().first()

        assert playlist_id is None

