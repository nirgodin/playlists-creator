from abc import ABC, abstractmethod
from base64 import b64encode
from http import HTTPStatus
from random import randint
from typing import Dict, List, Union
from unittest.mock import patch

from _pytest.fixtures import fixture
from aioresponses import aioresponses
from fastapi.openapi.models import Response
from genie_common.utils import random_alphanumeric_string, random_boolean
from genie_datastores.postgres.models import PlaylistEndpoint, CaseProgress, Case
from genie_datastores.postgres.operations import execute_query
from genie_datastores.postgres.testing import postgres_session
from sqlalchemy import select

from main import app
from server.component_factory import get_endpoint_controller_mapping, get_cases_manager
from server.consts.api_consts import ID
from server.consts.app_consts import ACCESS_CODE, PLAYLIST_DETAILS, PLAYLIST_NAME, PLAYLIST_DESCRIPTION, \
    IS_PUBLIC
from server.controllers.content_controllers.base_content_controller import BaseContentController
from server.data.case_status import CaseStatus
from server.data.playlist_creation_context import PlaylistCreationContext
from server.logic.cases_manager import CasesManager
from tests.server.integration.test_resources import TestResources
from tests.server.utils import random_image_bytes, build_spotify_url


class BasePlaylistControllerTest(ABC):
    @fixture(autouse=True, scope="class")
    async def set_up(self,
                     resources: TestResources,
                     endpoint: PlaylistEndpoint,
                     controller: BaseContentController,
                     cases_manager: CasesManager) -> None:
        endpoint_controller_mapping = {endpoint: controller}
        app.dependency_overrides[get_endpoint_controller_mapping] = lambda: endpoint_controller_mapping
        app.dependency_overrides[get_cases_manager] = lambda: cases_manager

        async with postgres_session(resources.engine):
            yield

    async def test_post(self,
                        payload: Dict[str, Union[str, dict]],
                        mock_responses: aioresponses,
                        expected_progress_statuses: List[CaseStatus],
                        endpoint: PlaylistEndpoint,
                        uris: List[str],
                        playlist_id: str,
                        resources: TestResources,
                        case_id: str):
        response = resources.client.post(
            url=f'api/playlist/{endpoint.value}',
            json=payload,
            auth=resources.auth
        )

        self._assert_expected_response(response, case_id)
        await self._assert_expected_case_progress_records(resources, expected_progress_statuses, case_id)
        await self._assert_expected_case_record(resources, case_id, playlist_id, endpoint)
        self._assert_expected_endpoints_calls(mock_responses, playlist_id, uris)

    @fixture(scope="class")
    @abstractmethod
    def controller(self, context: PlaylistCreationContext) -> BaseContentController:
        raise NotImplementedError

    @fixture(scope="class")
    @abstractmethod
    def endpoint(self) -> PlaylistEndpoint:
        raise NotImplementedError

    @fixture(scope="class")
    @abstractmethod
    def payload(self) -> Dict[str, Union[str, dict]]:
        raise NotImplementedError

    @fixture(scope="class")
    def case_id(self) -> str:
        with patch("server.logic.cases_manager.random_alphanumeric_string") as mock_random_alphanumeric_string:
            case_id = random_alphanumeric_string()
            mock_random_alphanumeric_string.return_value = case_id

            yield case_id

    @fixture(scope="class")
    def playlist_id(self) -> str:
        return random_alphanumeric_string()

    @fixture(scope="class")
    def user_id(self) -> str:
        return random_alphanumeric_string()

    @fixture(autouse=True, scope="class")
    def responses(self, mock_responses: aioresponses, user_id: str, playlist_id: str) -> None:
        """ In case you want to add more responses, use a dedicated `additional_responses` fixtures on child class """
        cover = b64encode(random_image_bytes()).decode("utf-8")
        mock_responses.get(
            url=build_spotify_url(["me"]),
            payload={ID: user_id}
        )
        mock_responses.post(
            url=build_spotify_url(["users", user_id, "playlists"]),
            payload={ID: playlist_id}
        )
        mock_responses.post(
            url=build_spotify_url(["playlists", playlist_id, "tracks"])
        )
        mock_responses.put(
            url=build_spotify_url(["playlists", playlist_id, "images"])
        )

        mock_responses.post(url='https://api.openai.com/v1/images/generations', payload={"data": [{"b64_json": cover}]})

        yield

    @fixture(scope="class")
    def uris(self) -> List[str]:
        n_elements = randint(1, 50)
        return [self._random_track_uri() for _ in range(n_elements)]

    @fixture(scope="class")
    @abstractmethod
    def expected_progress_statuses(self) -> List[CaseStatus]:
        raise NotImplementedError

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
    def _random_track_uri() -> str:
        return f"track:uri:{random_alphanumeric_string(32)}"

    @staticmethod
    async def _assert_expected_case_progress_records(resources: TestResources, expected_progress_statuses: List[CaseStatus], case_id: str) -> None:
        expected = [status.value for status in expected_progress_statuses]
        query = (
            select(CaseProgress.status)
            .where(CaseProgress.case_id == case_id)
            .order_by(CaseProgress.creation_date.asc())
        )
        query_result = await execute_query(engine=resources.engine, query=query)
        actual = query_result.scalars().all()

        assert actual == expected

    @staticmethod
    def _assert_expected_response(response: Response, case_id: str) -> None:
        assert response.status_code == HTTPStatus.CREATED.value
        assert response.json() == {"caseId": case_id}

    @staticmethod
    async def _assert_expected_case_record(resources: TestResources, case_id: str, playlist_id: str, endpoint: PlaylistEndpoint) -> None:
        query = (
            select(Case)
            .where(Case.id == case_id)
        )
        query_result = await execute_query(engine=resources.engine, query=query)

        actual = query_result.scalars().first()

        assert actual.endpoint == endpoint
        assert actual.playlist_id == playlist_id

    @staticmethod
    def _assert_expected_endpoints_calls(mock_responses: aioresponses, playlist_id: str, uris: List[str]) -> None:
        mock_responses.assert_called_with(
            url=f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks',
            json={"uris": uris},
            method="POST"
        )
        # mock_responses.assert_called_with(f'https://api.spotify.com/v1/playlists/{playlist_id}/images', method="POST")
