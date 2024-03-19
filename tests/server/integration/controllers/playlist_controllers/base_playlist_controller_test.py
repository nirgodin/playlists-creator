from abc import ABC, abstractmethod
from base64 import b64encode
from http import HTTPStatus
from random import randint
from typing import Dict, List
from unittest.mock import patch

from _pytest.fixtures import fixture
from aioresponses import aioresponses
from fastapi.openapi.models import Response
from genie_common.utils import random_alphanumeric_string, random_enum_value, random_boolean
from genie_datastores.postgres.models import PlaylistEndpoint, CaseProgress, Case
from genie_datastores.postgres.operations import execute_query
from genie_datastores.postgres.testing import postgres_session
from spotipyio.logic.authentication.spotify_session import SpotifySession
from spotipyio.logic.collectors.top_items_collectors.time_range import TimeRange
from sqlalchemy import select

from main import app
from server.component_factory import get_endpoint_controller_mapping, get_cases_manager
from server.consts.api_consts import ID
from server.consts.app_consts import ACCESS_CODE, PLAYLIST_DETAILS, TIME_RANGE, PLAYLIST_NAME, PLAYLIST_DESCRIPTION, \
    IS_PUBLIC
from server.consts.data_consts import ITEMS, URI
from server.controllers.content_controllers.base_content_controller import BaseContentController
from server.controllers.content_controllers.wrapped_controller import WrappedController
from server.data.case_status import CaseStatus
from server.data.playlist_creation_context import PlaylistCreationContext
from server.logic.cases_manager import CasesManager
from tests.server.integration.test_resources import TestResources
from tests.server.utils import generate_random_image_bytes


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

    @fixture
    @abstractmethod
    def controller(self, context: PlaylistCreationContext) -> BaseContentController:
        raise NotImplementedError

    @fixture
    @abstractmethod
    def endpoint(self) -> PlaylistEndpoint:
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
        cover = b64encode(generate_random_image_bytes()).decode("utf-8")
        mock_responses.get(url="https://api.spotify.com/v1/me", payload={ID: user_id})
        mock_responses.post(url=f'https://api.spotify.com/v1/users/{user_id}/playlists', payload={ID: playlist_id})
        mock_responses.post(url=f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks')
        mock_responses.post(url='https://api.openai.com/v1/images/generations', payload={"data": [{"b64_json": cover}]})
        mock_responses.put(url=f'https://api.spotify.com/v1/playlists/{playlist_id}/images')

        yield

    @staticmethod
    async def _assert_expected_case_progress_records(resources: TestResources, case_id: str) -> None:
        expected = [
            CaseStatus.CREATED,
            CaseStatus.TRACKS,
            CaseStatus.PLAYLIST,
            CaseStatus.COVER,
            CaseStatus.COMPLETED,
        ]
        query = (
            select(CaseProgress.status)
            .where(CaseProgress.case_id == case_id)
            .order_by(CaseProgress.creation_date.asc())
        )
        query_result = await execute_query(engine=resources.engine, query=query)
        actual = query_result.scalars().all()

        assert actual == [status.value for status in expected]

    @staticmethod
    def _assert_expected_response(response: Response, case_id: str) -> None:
        assert response.status_code == HTTPStatus.CREATED.value
        assert response.json() == {"caseId": case_id}

    @staticmethod
    async def _assert_expected_case_record(resources: TestResources, case_id: str, playlist_id: str) -> None:
        query = (
            select(Case)
            .where(Case.id == case_id)
        )
        query_result = await execute_query(engine=resources.engine, query=query)

        actual = query_result.scalars().first()

        assert actual.endpoint == PlaylistEndpoint.WRAPPED
        assert actual.playlist_id == playlist_id

    @staticmethod
    def _assert_expected_endpoints_calls(mock_responses: aioresponses, playlist_id: str,
                                         playlist_items: List[Dict[str, str]]) -> None:
        uris = [item[URI] for item in playlist_items]
        mock_responses.assert_called_with(
            url=f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks',
            json={"uris": uris},
            method="POST"
        )
        # mock_responses.assert_called_with(f'https://api.spotify.com/v1/playlists/{playlist_id}/images', method="POST")
