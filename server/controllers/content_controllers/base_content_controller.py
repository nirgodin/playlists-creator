from abc import ABC, abstractmethod
from tempfile import TemporaryDirectory
from typing import Optional

from aiohttp import ClientSession
from flask import request, Request, Response

from server.consts.app_consts import ACCESS_CODE, PLAYLIST_DETAILS
from server.data.playlist_creation_config import PlaylistCreationConfig
from server.data.playlist_resources import PlaylistResources
from server.data.spotify_grant_type import SpotifyGrantType
from server.logic.openai.openai_client import OpenAIClient
from server.logic.playlist_cover_photo_creator import PlaylistCoverPhotoCreator
from server.logic.playlists_creator import PlaylistsCreator
from server.tools.response_factory import ResponseFactory


class BaseContentController(ABC):
    def __init__(self, session: ClientSession):
        self._playlists_creator = PlaylistsCreator()
        self._playlist_cover_photo_creator = PlaylistCoverPhotoCreator()
        self._openai_client = OpenAIClient(session)

    async def post(self) -> Response:
        request_body = self._get_request_body(request)

        with TemporaryDirectory() as dir_path:
            return await self._execute_playlist_creation_process(request_body, dir_path)

    async def _execute_playlist_creation_process(self, request_body: dict, dir_path: str) -> Response:
        playlist_resources = await self._generate_playlist_resources(request_body, dir_path)
        if not playlist_resources.uris:
            return ResponseFactory.build_no_content_response()

        playlist_id = self._create_playlist(request_body, playlist_resources)
        if playlist_id is None:
            return ResponseFactory.build_authentication_failure_response()

        return ResponseFactory.build_success_response(playlist_id)

    @abstractmethod
    def _get_request_body(self, client_request: Request) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def _generate_playlist_resources(self, request_body: dict, dir_path: str) -> PlaylistResources:
        raise NotImplementedError

    @abstractmethod
    def _generate_playlist_cover(self, request_body: dict, image_path: str) -> None:
        raise NotImplementedError

    def _create_playlist(self, request_body: dict, playlist_resources: PlaylistResources) -> Optional[str]:
        config = PlaylistCreationConfig(
            access_code=request_body[ACCESS_CODE],
            playlist_details=request_body[PLAYLIST_DETAILS],
            grant_type=SpotifyGrantType.AUTHORIZATION_CODE,
            uris=playlist_resources.uris
        )
        if config.headers is None:
            return

        playlist_id = self._playlists_creator.create(config, retries_left=1)
        if playlist_id is None:
            return

        self._create_playlist_cover(request_body, playlist_id, config.headers, playlist_resources.cover_image_path)

        return playlist_id

    def _create_playlist_cover(self, request_body: dict, playlist_id: str, headers: dict, image_path: str) -> None:
        try:
            created_image_path = self._generate_playlist_cover(request_body, image_path)
            if created_image_path is None:
                return

            self._playlist_cover_photo_creator.put_playlist_cover(
                headers=headers,
                playlist_id=playlist_id,
                image_path=created_image_path
            )

        except:
            print('Failed to create playlist cover')
