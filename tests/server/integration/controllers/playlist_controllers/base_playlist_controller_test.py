from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import Dict, List, Union
from unittest.mock import patch

from _pytest.fixtures import fixture
from aiohttp import payload_type
from aioresponses import aioresponses
from fastapi.openapi.models import Response
from genie_common.utils import random_alphanumeric_string, random_boolean
from genie_datastores.postgres.models import PlaylistEndpoint, CaseProgress, Case
from genie_datastores.postgres.operations import execute_query
from genie_datastores.testing.postgres import postgres_session
from sqlalchemy import select

from server.component_factory import get_endpoint_controller_mapping, get_cases_manager
from server.consts.api_consts import ID
from server.consts.app_consts import ACCESS_CODE, PLAYLIST_DETAILS, PLAYLIST_NAME, PLAYLIST_DESCRIPTION, \
    IS_PUBLIC
from server.controllers.content_controllers.base_content_controller import BaseContentController
from server.data.case_status import CaseStatus
from server.data.playlist_creation_context import PlaylistCreationContext
from server.logic.cases_manager import CasesManager
from tests.server.integration.controllers.playlist_controllers.playlist_controller_test_context import \
    PlaylistControllerTestContext
from tests.server.integration.test_records import TestRecords
from tests.server.integration.test_resources import TestResources
from tests.server.utils import build_spotify_url, random_encoded_image


class BasePlaylistControllerTest(ABC):
    @fixture(autouse=True, scope="function")
    async def set_up(self,
                     endpoint: PlaylistEndpoint,
                     controller: BaseContentController,
                     cases_manager: CasesManager,
                     resources: TestResources,
                     records: TestRecords) -> None:
        endpoint_controller_mapping = {endpoint: controller}
        resources.app.dependency_overrides[get_endpoint_controller_mapping] = lambda: endpoint_controller_mapping
        resources.app.dependency_overrides[get_cases_manager] = lambda: cases_manager

        async with postgres_session(records.engine):
            await records.insert()
            yield

    @fixture(scope="function")
    def test_context(self,
                     payload: Dict[str, Union[str, dict]],
                     mock_responses: aioresponses,
                     expected_progress_statuses: List[CaseStatus],
                     endpoint: PlaylistEndpoint,
                     uris: List[str],
                     playlist_id: str,
                     resources: TestResources,
                     case_id: str) -> PlaylistControllerTestContext:
        return PlaylistControllerTestContext(
            case_id=case_id,
            endpoint=endpoint,
            expected_progress_statuses=expected_progress_statuses,
            mock_responses=mock_responses,
            payload=payload,
            playlist_id=playlist_id,
            resources=resources,
            uris=uris
        )

    @fixture(scope="class")
    @abstractmethod
    def controller(self, context: PlaylistCreationContext) -> BaseContentController:
        raise NotImplementedError

    @fixture(scope="class")
    @abstractmethod
    def endpoint(self) -> PlaylistEndpoint:
        raise NotImplementedError

    @fixture(scope="function")
    @abstractmethod
    def payload(self) -> Dict[str, Union[str, dict]]:
        raise NotImplementedError

    @fixture(scope="function")
    @abstractmethod
    def expected_progress_statuses(self) -> List[CaseStatus]:
        raise NotImplementedError

    @fixture(scope="class")
    @abstractmethod
    def uris(self) -> List[str]:
        raise NotImplementedError

    @fixture(scope="function")
    def case_id(self) -> str:
        with patch("server.logic.cases_manager.random_alphanumeric_string") as mock_random_alphanumeric_string:
            case_id = random_alphanumeric_string()
            mock_random_alphanumeric_string.return_value = case_id

            yield case_id

    @fixture(scope="function")
    def playlist_id(self) -> str:
        return random_alphanumeric_string()

    @fixture(scope="function")
    def user_id(self) -> str:
        return random_alphanumeric_string()

    @fixture(autouse=True, scope="function")
    def responses(self, mock_responses: aioresponses, user_id: str, playlist_id: str) -> None:
        """ In case you want to add more responses, use a dedicated `additional_responses` fixtures on child class """
        cover = random_encoded_image()
        mock_responses.get(
            url=build_spotify_url(["me"]),
            payload={ID: user_id}
        )
        mock_responses.post(
            url=build_spotify_url(["users", user_id, "playlists"]),
            payload={ID: playlist_id}
        )
        mock_responses.post(
            url=build_spotify_url(["playlists", playlist_id, "tracks"]),
            payload={"snapshot_id": random_alphanumeric_string()}
        )
        mock_responses.put(
            url=build_spotify_url(["playlists", playlist_id, "images"])
        )

        mock_responses.post(url='https://api.openai.com/v1/images/generations', payload={"data": [{"b64_json": cover}]})

        yield

    @staticmethod
    def _get_basic_request_payload() -> Dict[str, Union[str, dict]]:
        return {
            ACCESS_CODE: random_alphanumeric_string(),
            PLAYLIST_DETAILS: {
                PLAYLIST_NAME: random_alphanumeric_string(),
                PLAYLIST_DESCRIPTION: random_alphanumeric_string(),
                IS_PUBLIC: random_boolean()
            }
        }

    @staticmethod
    def _request(test_context: PlaylistControllerTestContext) -> Response:
        return test_context.resources.client.post(
            url=f'api/playlist/{test_context.endpoint.value}',
            json=test_context.payload,
            auth=test_context.resources.auth
        )

    async def _assert_expected_base_controller_logic(self, response: Response, test_context: PlaylistControllerTestContext) -> None:
        self._assert_expected_response(response, test_context.case_id)
        await self._assert_expected_case_progress_records(test_context)
        await self._assert_expected_case_record(test_context)
        self._assert_expected_endpoints_calls(test_context)

    @staticmethod
    async def _assert_expected_case_progress_records(test_context: PlaylistControllerTestContext) -> None:
        expected = [status.value for status in test_context.expected_progress_statuses]
        query = (
            select(CaseProgress.status)
            .where(CaseProgress.case_id == test_context.case_id)
            .order_by(CaseProgress.creation_date.asc())
        )
        query_result = await execute_query(engine=test_context.resources.engine, query=query)
        actual = query_result.scalars().all()

        assert actual == expected

    @staticmethod
    def _assert_expected_response(response: Response, case_id: str) -> None:
        assert response.status_code == HTTPStatus.CREATED.value
        assert response.json() == {"caseId": case_id}

    @staticmethod
    async def _assert_expected_case_record(test_context: PlaylistControllerTestContext) -> None:
        query = (
            select(Case)
            .where(Case.id == test_context.case_id)
        )
        query_result = await execute_query(engine=test_context.resources.engine, query=query)

        actual = query_result.scalars().first()

        assert actual.endpoint == test_context.endpoint
        assert actual.playlist_id == test_context.playlist_id

    @staticmethod
    def _assert_expected_endpoints_calls(test_context: PlaylistControllerTestContext) -> None:
        test_context.mock_responses.assert_called_with(
            url=f'https://api.spotify.com/v1/playlists/{test_context.playlist_id}/tracks',
            json={"position": None, "uris": test_context.uris},
            method="POST"
        )
        # mock_responses.assert_called_with(f'https://api.spotify.com/v1/playlists/{playlist_id}/images', method="POST")
