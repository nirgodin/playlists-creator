from base64 import b64decode
from typing import Optional

from genie_common.models.openai import DallEModel, ImageSize
from spotipyio import SpotifyClient

from server.controllers.content_controllers.base_content_controller import BaseContentController
from server.data.content_controllers.playlists_merger_request import PlaylistsMergerRequest
from server.data.playlist_resources import PlaylistResources
from server.logic.playlists_merger import PlaylistsMerger
from server.utils.image_utils import current_timestamp_image_path, save_image_from_bytes


class PlaylistsMergerController(BaseContentController):
    async def _generate_playlist_resources(self,
                                           case_id: str,
                                           request_body: dict,
                                           dir_path: str,
                                           spotify_client: SpotifyClient) -> PlaylistResources:
        request = PlaylistsMergerRequest.model_validate(request_body)  # TODO: Remove duplicate model validation once all components use pydantic models
        uris = await PlaylistsMerger.merge(
            spotify_client=spotify_client,
            ids=request.ids,
            shuffle_items=request.shuffle
        )

        return PlaylistResources(
            uris=uris,
            cover_image_path=current_timestamp_image_path(dir_path)
        )

    async def _generate_playlist_cover(self, request_body: dict, image_path: str) -> Optional[str]:
        request = PlaylistsMergerRequest.model_validate(request_body)
        encoded_image: str = await self._context.openai_client.images_generation.collect(  # TODO: Extract flow to common component shared with Prompt controller
            prompt=request.cover_photo_prompt,
            model=DallEModel.DALLE_3,
            n=1,
            size=ImageSize.P1024
        )
        image: bytes = b64decode(encoded_image)
        save_image_from_bytes(image, image_path)

        return image_path
