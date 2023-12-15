from genie_common.utils import safe_nested_get
from spotipyio import SpotifyClient
from spotipyio.logic.collectors.top_items_collectors.items_type import ItemsType
from spotipyio.logic.collectors.top_items_collectors.time_range import TimeRange

from server.consts.app_consts import PLAYLIST_DETAILS, TIME_RANGE
from server.consts.data_consts import URI, ITEMS
from server.controllers.content_controllers.base_content_controller import BaseContentController
from server.data.playlist_resources import PlaylistResources


class WrappedController(BaseContentController):
    async def _generate_playlist_resources(self,
                                           request_body: dict,
                                           dir_path: str,
                                           spotify_client: SpotifyClient) -> PlaylistResources:
        raw_time_range = safe_nested_get(request_body, [PLAYLIST_DETAILS, TIME_RANGE], TimeRange.SHORT_TERM.value)
        response = await spotify_client.current_user.top_items.run(
            items_type=ItemsType.TRACKS,
            time_range=TimeRange(raw_time_range),
            limit=50
        )
        uris = [item[URI] for item in response[ITEMS]]

        return PlaylistResources(uris=uris, cover_image_path=None)

    async def _generate_playlist_cover(self, request_body: dict, image_path: str) -> None:  # TODO: Implement
        raise NotImplementedError
