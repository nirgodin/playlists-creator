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
from server.controllers.content_controllers.wrapped_controller import WrappedController
from server.data.case_status import CaseStatus
from server.data.playlist_creation_context import PlaylistCreationContext
from server.logic.cases_manager import CasesManager
from tests.server.integration.test_resources import TestResources
from tests.server.utils import generate_random_image_bytes


class TestWrappedController:
    @fixture(autouse=True, scope="class")
    async def set_up(self, resources: TestResources, wrapped_controller: WrappedController,
                     cases_manager: CasesManager) -> None:
        endpoint_controller_mapping = {PlaylistEndpoint.WRAPPED: wrapped_controller}
        app.dependency_overrides[get_endpoint_controller_mapping] = lambda: endpoint_controller_mapping
        app.dependency_overrides[get_cases_manager] = lambda: cases_manager

        async with postgres_session(resources.engine):
            yield

    async def test_post(self,
                        mock_responses: aioresponses,
                        playlist_items: List[Dict[str, str]],
                        playlist_id: str,
                        time_range: str,
                        spotify_session: SpotifySession,
                        resources: TestResources,
                        case_id: str):
        request = {
            ACCESS_CODE: random_alphanumeric_string(),
            PLAYLIST_DETAILS: {
                TIME_RANGE: time_range,
                PLAYLIST_NAME: random_alphanumeric_string(),
                PLAYLIST_DESCRIPTION: random_alphanumeric_string(),
                IS_PUBLIC: random_boolean()
            }
        }

        response = resources.client.post(
            url='api/playlist/wrapped',
            json=request,
            auth=resources.auth
        )

        self._assert_expected_response(response, case_id)
        await self._assert_expceted_case_progress_records(resources, case_id)
        await self._assert_expected_case_record(resources, case_id, playlist_id)
        self._assert_expected_endpoints_calls(mock_responses, playlist_id, playlist_items)

    @fixture(autouse=True, scope="class")
    def responses(self, mock_responses: aioresponses, user_id: str, playlist_id: str, time_range: str, playlist_items: List[str]):
        url = f"https://api.spotify.com/v1/me/top/tracks?limit=50&time_range={time_range}"
        cover = b64encode(generate_random_image_bytes()).decode("utf-8")
        mock_responses.get(url=url, payload={ITEMS: playlist_items})
        mock_responses.get(url="https://api.spotify.com/v1/me", payload={ID: user_id})
        mock_responses.post(url=f'https://api.spotify.com/v1/users/{user_id}/playlists', payload={ID: playlist_id})
        mock_responses.post(url=f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks')
        mock_responses.post(url='https://api.openai.com/v1/images/generations', payload={"data": [{"b64_json": cover}]})
        mock_responses.put(url=f'https://api.spotify.com/v1/playlists/{playlist_id}/images')

        yield

    @fixture(scope="class")
    def playlist_id(self) -> str:
        return random_alphanumeric_string()

    @fixture(scope="class")
    def user_id(self) -> str:
        return random_alphanumeric_string()

    @fixture(scope="class")
    def time_range(self) -> str:
        time_range = random_enum_value(TimeRange)
        return time_range.value

    @fixture(scope="class")
    def playlist_items(self) -> List[Dict[str, str]]:
        n_items = randint(1, 50)
        return [self._random_playlist_item() for _ in range(n_items)]

    @staticmethod
    def _random_playlist_item() -> Dict[str, str]:
        return {URI: f"track:uri:{random_alphanumeric_string(32)}"}

    @fixture(scope="class")
    def case_id(self) -> str:
        with patch("server.logic.cases_manager.random_alphanumeric_string") as mock_random_alphanumeric_string:
            case_id = random_alphanumeric_string()
            mock_random_alphanumeric_string.return_value = case_id

            yield case_id

    @fixture(scope="class")
    def wrapped_controller(self, context: PlaylistCreationContext) -> WrappedController:
        return WrappedController(context)

    @staticmethod
    async def _assert_expceted_case_progress_records(resources: TestResources, case_id: str) -> None:
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
    def _assert_expected_endpoints_calls(mock_responses: aioresponses, playlist_id: str, playlist_items: List[Dict[str, str]]) -> None:
        uris = [item[URI] for item in playlist_items]
        mock_responses.assert_called_with(
            url=f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks',
            json={"uris": uris},
            method="POST"
        )
        # mock_responses.assert_called_with(f'https://api.spotify.com/v1/playlists/{playlist_id}/images', method="POST")
