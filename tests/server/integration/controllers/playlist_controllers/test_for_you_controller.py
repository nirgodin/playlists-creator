from random import randint
from typing import Dict, List, Union
from unittest.mock import AsyncMock

from _pytest.fixtures import fixture
from aioresponses import aioresponses
from genie_datastores.postgres.models import PlaylistEndpoint
from spotipyio.logic.collectors.top_items_collectors.time_range import TimeRange

from server.consts.data_consts import ITEMS
from server.controllers.content_controllers.for_you_controller import ForYouController
from server.data.case_status import CaseStatus
from server.data.playlist_creation_context import PlaylistCreationContext
from server.data.playlist_resources import PlaylistResources
from server.logic.data_collection.spotify_playlist_details_collector import PlaylistDetailsCollector
from server.logic.playlist_imitation.playlist_imitator import PlaylistImitator
from tests.server.integration.controllers.playlist_controllers.base_playlist_controller_test import \
    BasePlaylistControllerTest
from tests.server.integration.controllers.playlist_controllers.playlist_controller_test_context import \
    PlaylistControllerTestContext
from tests.server.utils import build_spotify_url, random_playlist_item, random_track_uri


class TestForYouController(BasePlaylistControllerTest):
    async def test_post(self, test_context: PlaylistControllerTestContext):
        response = self._request(test_context)
        await self._assert_expected_base_controller_logic(response, test_context)

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

    @fixture(scope="class")
    def uris(self) -> List[str]:
        n_elements = randint(1, 50)
        return [random_track_uri() for _ in range(n_elements)]

    @fixture(autouse=True, scope="class")
    def additional_responses(self, uris: List[str], mock_responses: aioresponses) -> None:
        time_range = TimeRange.MEDIUM_TERM.value
        playlist_items = [random_playlist_item(uri) for uri in uris]
        url = build_spotify_url(
            routes=["me", "top", "tracks"],
            params={"limit": 50, "time_range": time_range}
        )
        mock_responses.get(
            url=url,
            payload={ITEMS: playlist_items}
        )

        yield
