from base64 import b64decode
from typing import Optional

from genie_common.models.openai import DallEModel, ImageSize
from genie_common.utils import safe_nested_get
from spotipyio import SpotifyClient
from spotipyio.models import ItemsType, TimeRange

from server.consts.app_consts import PLAYLIST_DETAILS, TIME_RANGE
from server.consts.data_consts import URI, ITEMS
from server.controllers.content_controllers.base_content_controller import BaseContentController
from server.data.case_status import CaseStatus
from server.data.playlist_resources import PlaylistResources
from server.utils.image_utils import save_image_from_bytes, current_timestamp_image_path


class WrappedController(BaseContentController):
    async def _generate_playlist_resources(self,
                                           case_id: str,
                                           request_body: dict,
                                           dir_path: str,
                                           spotify_client: SpotifyClient) -> PlaylistResources:
        async with self._context.case_progress_reporter.report(case_id=case_id, status=CaseStatus.TRACKS):
            raw_time_range = safe_nested_get(
                dct=request_body,
                paths=[PLAYLIST_DETAILS, TIME_RANGE],
                default=TimeRange.SHORT_TERM.value
            )
            response = await spotify_client.current_user.top_items.run(
                items_type=ItemsType.TRACKS,
                time_range=TimeRange(raw_time_range),
                limit=50
            )
            uris = [item[URI] for item in response[ITEMS]]
            image_path = current_timestamp_image_path(dir_path)

            return PlaylistResources(uris=uris, cover_image_path=image_path)

    async def _generate_playlist_cover(self, request_body: dict, image_path: str) -> Optional[str]:
        encoded_image: str = await self._context.openai_client.images_generation.collect(
            prompt="Songs I have been playing on repeat lately, digital art",
            model=DallEModel.DALLE_3,
            n=1,
            size=ImageSize.P1024
        )
        image: bytes = b64decode(encoded_image)
        save_image_from_bytes(image, image_path)

        return image_path
