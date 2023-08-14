from abc import ABC, abstractmethod
from tempfile import TemporaryDirectory
from typing import Optional

from aiohttp import ClientSession
from starlette.responses import JSONResponse

from server.consts.api_consts import ACCESS_TOKEN
from server.consts.app_consts import ACCESS_CODE, PLAYLIST_DETAILS
from server.data.playlist_creation_config import PlaylistCreationConfig
from server.data.playlist_resources import PlaylistResources
from server.data.spotify_grant_type import SpotifyGrantType
from server.logic.access_token_generator import AccessTokenGenerator
from server.logic.openai.openai_client import OpenAIClient
from server.logic.playlist_cover_photo_creator import PlaylistCoverPhotoCreator
from server.logic.playlists_creator import PlaylistsCreator
from server.tools.response_factory import ResponseFactory
from server.utils.general_utils import build_spotify_headers


class BaseContentController(ABC):
    def __init__(self,
                 playlists_creator: PlaylistsCreator,
                 playlists_cover_photo_creator: PlaylistCoverPhotoCreator,
                 openai_client: OpenAIClient,
                 access_token_generator: AccessTokenGenerator):
        self._playlists_creator = playlists_creator
        self._playlist_cover_photo_creator = playlists_cover_photo_creator
        self._openai_client = openai_client
        self._access_token_generator = access_token_generator

    async def post(self, request) -> JSONResponse:
        request_body = self._get_request_body(request)

        with TemporaryDirectory() as dir_path:
            return await self._execute_playlist_creation_process(request_body, dir_path)

    async def _execute_playlist_creation_process(self, request_body: dict, dir_path: str) -> JSONResponse:
        playlist_resources = await self._generate_playlist_resources(request_body, dir_path)
        if not playlist_resources.uris:
            return ResponseFactory.build_no_content_response()

        playlist_id = await self._create_playlist(request_body, playlist_resources)
        if playlist_id is None:
            return ResponseFactory.build_authentication_failure_response()

        return ResponseFactory.build_success_response(playlist_id)

    @abstractmethod
    def _get_request_body(self, request: dict) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def _generate_playlist_resources(self, request_body: dict, dir_path: str) -> PlaylistResources:
        raise NotImplementedError

    @abstractmethod
    async def _generate_playlist_cover(self, request_body: dict, image_path: str) -> None:
        raise NotImplementedError

    async def _create_playlist(self, request_body: dict, playlist_resources: PlaylistResources) -> Optional[str]:
        access_code = request_body[ACCESS_CODE]
        access_token_generator_response = await self._access_token_generator.generate(
            grant_type=SpotifyGrantType.AUTHORIZATION_CODE,
            access_code=access_code
        )
        bearer_token = access_token_generator_response.get(ACCESS_TOKEN)
        headers = build_spotify_headers(bearer_token)
        if headers is None:
            return

        config = PlaylistCreationConfig(
            access_code=request_body[ACCESS_CODE],
            playlist_details=request_body[PLAYLIST_DETAILS],
            grant_type=SpotifyGrantType.AUTHORIZATION_CODE,
            uris=playlist_resources.uris,
            access_token_generator_response=access_token_generator_response,
            headers=headers
        )
        playlist_id = await self._playlists_creator.create(config, retries_left=1)

        if playlist_id is not None:
            await self._create_playlist_cover(request_body, playlist_id, config.headers, playlist_resources.cover_image_path)
            return playlist_id

    async def _create_playlist_cover(self, request_body: dict, playlist_id: str, headers: dict, image_path: str) -> None:
        try:
            created_image_path = await self._generate_playlist_cover(request_body, image_path)

            if created_image_path is not None:
                await self._playlist_cover_photo_creator.put_playlist_cover(
                    headers=headers,
                    playlist_id=playlist_id,
                    image_path=created_image_path
                )

        except Exception as e:
            print('Failed to create playlist cover')
