from random import randint
from typing import Dict, List, Union

from _pytest.fixtures import fixture
from aioresponses import aioresponses
from genie_common.utils import random_enum_value
from genie_datastores.postgres.models import PlaylistEndpoint
from spotipyio.models import TimeRange

from server.consts.app_consts import PLAYLIST_DETAILS, TIME_RANGE
from server.consts.data_consts import ITEMS
from server.controllers.content_controllers.wrapped_controller import WrappedController
from server.data.case_status import CaseStatus
from server.data.playlist_creation_context import PlaylistCreationContext
from tests.server.integration.controllers.playlist_controllers.base_playlist_controller_test import \
    BasePlaylistControllerTest
from tests.server.integration.controllers.playlist_controllers.playlist_controller_test_context import \
    PlaylistControllerTestContext
from tests.server.utils import build_spotify_url, random_playlist_item, random_track_uri


class TestWrappedController(BasePlaylistControllerTest):
    async def test_post(self, test_context: PlaylistControllerTestContext):
        response = self._request(test_context)
        await self._assert_expected_base_controller_logic(response, test_context)

    @fixture(scope="class")
    def controller(self, context: PlaylistCreationContext) -> WrappedController:
        return WrappedController(context)

    @fixture(scope="class")
    def endpoint(self) -> PlaylistEndpoint:
        return PlaylistEndpoint.WRAPPED

    @fixture(scope="function")
    def expected_progress_statuses(self) -> List[CaseStatus]:
        return [
            CaseStatus.CREATED,
            CaseStatus.TRACKS,
            CaseStatus.PLAYLIST,
            CaseStatus.COVER,
            CaseStatus.COMPLETED,
        ]

    @fixture(scope="function")
    def payload(self, time_range: str) -> Dict[str, Union[str, dict]]:
        payload = self._get_basic_request_payload()
        payload[PLAYLIST_DETAILS][TIME_RANGE] = time_range

        return payload

    @fixture(autouse=True, scope="function")
    def additional_responses(self, uris: List[str], time_range: str, mock_responses: aioresponses) -> None:
        playlist_items = [random_playlist_item(uri) for uri in uris]
        mock_responses.get(
            url=build_spotify_url(["me", "top", "tracks"], params={"limit": 50, "time_range": time_range}),
            payload={ITEMS: playlist_items}
        )

        yield

    @fixture(scope="class")
    def time_range(self) -> str:
        time_range = random_enum_value(TimeRange)
        return time_range.value

    @fixture(scope="class")
    def uris(self) -> List[str]:
        n_elements = randint(1, 50)
        return [random_track_uri() for _ in range(n_elements)]
