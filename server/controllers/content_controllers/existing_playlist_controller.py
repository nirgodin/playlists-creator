from typing import Optional

from server.consts.app_consts import PLAYLIST_DETAILS, EXISTING_PLAYLIST
from server.controllers.content_controllers.base_content_controller import BaseContentController
from server.data.playlist_resources import PlaylistResources
from server.logic.access_token_generator import AccessTokenGenerator
from server.logic.openai.openai_client import OpenAIClient
from server.logic.playlist_cover_photo_creator import PlaylistCoverPhotoCreator
from server.logic.playlist_imitation.playlist_imitator import PlaylistImitator
from server.logic.playlists_creator import PlaylistsCreator


class ExistingPlaylistController(BaseContentController):
    def __init__(self,
                 playlists_creator: PlaylistsCreator,
                 playlists_cover_photo_creator: PlaylistCoverPhotoCreator,
                 openai_client: OpenAIClient,
                 access_token_generator: AccessTokenGenerator,
                 playlists_imitator: PlaylistImitator):
        super().__init__(playlists_creator, playlists_cover_photo_creator, openai_client, access_token_generator)
        self._playlist_imitator = playlists_imitator

    async def _generate_playlist_resources(self, request_body: dict, dir_path: str) -> PlaylistResources:
        existing_playlist_url = request_body[PLAYLIST_DETAILS][EXISTING_PLAYLIST]
        return await self._playlist_imitator.imitate_playlist(existing_playlist_url, dir_path)

    async def _generate_playlist_cover(self, request_body: dict, image_path: str) -> Optional[str]:
        return await self._openai_client.variate_image(image_path, image_path)
