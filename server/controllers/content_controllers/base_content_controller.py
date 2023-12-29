from abc import ABC, abstractmethod
from io import BytesIO
from tempfile import TemporaryDirectory
from typing import Optional

from PIL import Image
from fastapi.security import HTTPBasicCredentials
from genie_common.openai import OpenAIClient
from genie_common.tools.logs import logger
from spotipyio import SpotifyClient
from starlette.responses import JSONResponse

from server.consts.app_consts import PLAYLIST_DETAILS
from server.data.playlist_creation_config import PlaylistCreationConfig
from server.data.playlist_resources import PlaylistResources
from server.logic.playlists_creator import PlaylistsCreator
from server.tools.authenticator import Authenticator
from server.tools.response_factory import ResponseFactory
from server.utils.spotify_utils import build_spotify_client


class BaseContentController(ABC):
    def __init__(self, authenticator: Authenticator, playlists_creator: PlaylistsCreator, openai_client: OpenAIClient):
        self._authenticator = authenticator
        self._playlists_creator = playlists_creator
        self._openai_client = openai_client

    async def post(self, request_body: dict, credentials: HTTPBasicCredentials) -> JSONResponse:
        logger.info("Received request", extra={"controller": self.__class__.__name__})
        self._authenticator.authenticate(credentials)

        with TemporaryDirectory() as dir_path:
            async with build_spotify_client(request_body) as spotify_client:
                return await self._execute_playlist_creation_process(request_body, dir_path, spotify_client)

    async def _execute_playlist_creation_process(self,
                                                 request_body: dict,
                                                 dir_path: str,
                                                 spotify_client: SpotifyClient) -> JSONResponse:
        logger.info("Starting to execute playlists creation process")
        playlist_resources = await self._generate_playlist_resources(request_body, dir_path, spotify_client)
        if not playlist_resources.uris:
            return ResponseFactory.build_no_content_response()

        playlist_id = await self._create_playlist(request_body, playlist_resources, spotify_client)
        if playlist_id is None:
            return ResponseFactory.build_authentication_failure_response()

        return ResponseFactory.build_success_response(playlist_id)

    @abstractmethod
    async def _generate_playlist_resources(self,
                                           request_body: dict,
                                           dir_path: str,
                                           spotify_client: SpotifyClient) -> PlaylistResources:
        raise NotImplementedError

    @abstractmethod
    async def _generate_playlist_cover(self, request_body: dict, image_path: str) -> Optional[str]:
        raise NotImplementedError

    async def _create_playlist(self,
                               request_body: dict,
                               playlist_resources: PlaylistResources,
                               spotify_client: SpotifyClient) -> Optional[str]:
        config = PlaylistCreationConfig(
            spotify_client=spotify_client,
            playlist_details=request_body[PLAYLIST_DETAILS],
            uris=playlist_resources.uris,
        )
        playlist_id = await self._playlists_creator.create(config)

        if playlist_id is not None:
            await self._create_playlist_cover(request_body, playlist_id, config, playlist_resources.cover_image_path)
            return playlist_id

    async def _create_playlist_cover(self,
                                     request_body: dict,
                                     playlist_id: str,
                                     config: PlaylistCreationConfig,
                                     image_path: str) -> None:
        try:
            created_image_path = await self._generate_playlist_cover(request_body, image_path)

            with open(created_image_path, "rb") as f:
                image = f.read()

            await config.spotify_client.playlists.update_cover.run(playlist_id, image)

        except Exception as e:
            print('Failed to create playlist cover')
