from typing import Optional

from flask import Request

from server.consts.app_consts import PLAYLIST_DETAILS, EXISTING_PLAYLIST
from server.controllers.content_controllers.base_content_controller import BaseContentController
from server.data.playlist_resources import PlaylistResources
from server.logic.playlist_imitation.playlist_imitator import PlaylistImitator


class ExistingPlaylistController(BaseContentController):
    def __init__(self):
        super().__init__()
        self._playlist_imitator = PlaylistImitator()

    def _get_request_body(self, client_request: Request) -> dict:
        return client_request.get_json()

    async def _generate_playlist_resources(self, request_body: dict, dir_path: str) -> PlaylistResources:
        existing_playlist_url = request_body[PLAYLIST_DETAILS][EXISTING_PLAYLIST]
        return await self._playlist_imitator.imitate_playlist(existing_playlist_url, dir_path)

    def _generate_playlist_cover(self, request_body: dict, image_path: str) -> Optional[str]:
        return self._dalle_adapter.variate_image(image_path, image_path)
