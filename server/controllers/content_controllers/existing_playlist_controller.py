import asyncio
from typing import List, Optional

from flask import Request

from server.consts.app_consts import PLAYLIST_DETAILS, EXISTING_PLAYLIST
from server.controllers.content_controllers.base_content_controller import BaseContentController
from server.logic.playlist_imitation.playlist_imitator import PlaylistImitator


class ExistingPlaylistController(BaseContentController):
    def __init__(self):
        super().__init__()
        self._playlist_imitator = PlaylistImitator()

    def _get_request_body(self, client_request: Request) -> dict:
        return client_request.get_json()

    def _generate_tracks_uris(self, request_body: dict) -> Optional[List[str]]:
        existing_playlist_url = request_body[PLAYLIST_DETAILS][EXISTING_PLAYLIST]
        imitator_response = asyncio.run(self._playlist_imitator.imitate_playlist(existing_playlist_url))

        return imitator_response

    def _generate_playlist_cover_prompt(self, request_body: dict) -> str:
        raise  # TODO: Rethink how to generate cover here
