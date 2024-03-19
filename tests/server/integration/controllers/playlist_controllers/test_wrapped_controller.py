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
from tests.server.integration.controllers.playlist_controllers.base_playlist_controller_test import \
    BasePlaylistControllerTest
from tests.server.integration.test_resources import TestResources
from tests.server.utils import generate_random_image_bytes


class TestWrappedController(BasePlaylistControllerTest):
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
        await self._assert_expected_case_progress_records(resources, case_id)
        await self._assert_expected_case_record(resources, case_id, playlist_id)
        self._assert_expected_endpoints_calls(mock_responses, playlist_id, playlist_items)

    @fixture(scope="class")
    def controller(self, context: PlaylistCreationContext) -> WrappedController:
        return WrappedController(context)

    @fixture(scope="class")
    def endpoint(self) -> PlaylistEndpoint:
        return PlaylistEndpoint.WRAPPED

    @fixture(autouse=True, scope="class")
    def additional_responses(self, mock_responses: aioresponses, time_range: str, playlist_items: List[str]) -> None:
        url = f"https://api.spotify.com/v1/me/top/tracks?limit=50&time_range={time_range}"
        mock_responses.get(url=url, payload={ITEMS: playlist_items})

        yield

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
