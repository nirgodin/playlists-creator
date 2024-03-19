from random import randint
from typing import Dict, List, Union

from _pytest.fixtures import fixture
from aioresponses import aioresponses
from genie_common.utils import random_alphanumeric_string, random_enum_value, random_boolean
from genie_datastores.postgres.models import PlaylistEndpoint
from spotipyio.logic.authentication.spotify_session import SpotifySession
from spotipyio.logic.collectors.top_items_collectors.time_range import TimeRange

from server.consts.app_consts import ACCESS_CODE, PLAYLIST_DETAILS, TIME_RANGE, PLAYLIST_NAME, PLAYLIST_DESCRIPTION, \
    IS_PUBLIC
from server.consts.data_consts import ITEMS, URI
from server.controllers.content_controllers.wrapped_controller import WrappedController
from server.data.case_status import CaseStatus
from server.data.playlist_creation_context import PlaylistCreationContext
from tests.server.integration.controllers.playlist_controllers.base_playlist_controller_test import \
    BasePlaylistControllerTest
from tests.server.integration.test_resources import TestResources


class TestWrappedController(BasePlaylistControllerTest):
    def controller(self, context: PlaylistCreationContext) -> WrappedController:
        return WrappedController(context)

    @fixture(scope="class")
    def endpoint(self) -> PlaylistEndpoint:
        return PlaylistEndpoint.WRAPPED

    @fixture(scope="class")
    def expected_progress_statuses(self) -> List[CaseStatus]:
        return [
            CaseStatus.CREATED,
            CaseStatus.TRACKS,
            CaseStatus.PLAYLIST,
            CaseStatus.COVER,
            CaseStatus.COMPLETED,
        ]

    @fixture(scope="class")
    def payload(self, time_range: str) -> Dict[str, Union[str, dict]]:
        payload = self._get_basic_request_payload()
        payload[PLAYLIST_DETAILS][TIME_RANGE] = time_range

        return payload

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
    def playlist_items(self, uris: List[str]) -> List[Dict[str, str]]:
        return [self._random_playlist_item(uri) for uri in uris]

    @staticmethod
    def _random_playlist_item(uri: str) -> Dict[str, str]:
        return {URI: uri}
