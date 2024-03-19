from unittest.mock import AsyncMock

from _pytest.fixtures import fixture
from genie_datastores.postgres.models import PlaylistEndpoint

from server.controllers.content_controllers.for_you_controller import ForYouController
from server.data.case_status import CaseStatus
from server.data.playlist_creation_context import PlaylistCreationContext
from server.data.playlist_resources import PlaylistResources
from server.logic.data_collection.spotify_playlist_details_collector import PlaylistDetailsCollector
from server.logic.playlist_imitation.playlist_imitator import PlaylistImitator
from tests.server.integration.controllers.playlist_controllers.base_playlist_controller_test import \
    BasePlaylistControllerTest
from random import randint
from typing import Dict, List, Union

from _pytest.fixtures import fixture
from aioresponses import aioresponses
from genie_common.utils import random_alphanumeric_string, random_enum_value, random_boolean, random_string_array
from genie_datastores.postgres.models import PlaylistEndpoint
from spotipyio.logic.authentication.spotify_session import SpotifySession
from spotipyio.logic.collectors.top_items_collectors.time_range import TimeRange

from server.consts.app_consts import ACCESS_CODE, PLAYLIST_DETAILS, TIME_RANGE, PLAYLIST_NAME, PLAYLIST_DESCRIPTION, \
    IS_PUBLIC
from server.consts.data_consts import ITEMS, URI
from server.controllers.content_controllers.wrapped_controller import WrappedController
from server.data.playlist_creation_context import PlaylistCreationContext
from tests.server.integration.controllers.playlist_controllers.base_playlist_controller_test import \
    BasePlaylistControllerTest
from tests.server.integration.test_resources import TestResources


class TestForYouController(BasePlaylistControllerTest):
    @fixture(scope="class")
    def controller(self, uris: List[str], context: PlaylistCreationContext) -> ForYouController:
        mock_playlist_imitator = AsyncMock(PlaylistImitator)
        mock_playlist_imitator.imitate_playlist.return_value = PlaylistResources(
            uris=uris,
            cover_image_path=""
        )
        return ForYouController(
            context=context,
            playlists_imitator=mock_playlist_imitator,
            playlist_details_collector=AsyncMock(PlaylistDetailsCollector)
        )

    @fixture(scope="class")
    def endpoint(self) -> PlaylistEndpoint:
        return PlaylistEndpoint.FOR_YOU

    @fixture(scope="class")
    def expected_progress_statuses(self) -> List[CaseStatus]:
        return [
            CaseStatus.CREATED,
            CaseStatus.PLAYLIST,
            CaseStatus.COVER,
            CaseStatus.COMPLETED,
        ]

    @fixture(scope="class")
    def payload(self) -> Dict[str, Union[str, dict]]:
        return self._get_basic_request_payload()

    @fixture(autouse=True, scope="class")
    def additional_responses(self, mock_responses: aioresponses, time_range: str, playlist_items: List[str]) -> None:
        url = f"https://api.spotify.com/v1/me/top/tracks?limit=50&time_range={time_range}"
        mock_responses.get(url=url, payload={ITEMS: playlist_items})

        yield

    @fixture(scope="class")
    def time_range(self) -> str:
        return TimeRange.MEDIUM_TERM.value  # TODO: Should not be hard-coded

    @fixture(scope="class")
    def playlist_items(self, uris: List[str]) -> List[Dict[str, str]]:
        return [self._random_playlist_item(uri) for uri in uris]

    @staticmethod
    def _random_playlist_item(uri: str) -> Dict[str, str]:
        return {URI: uri}
