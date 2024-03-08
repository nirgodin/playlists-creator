from abc import ABC, abstractmethod
from tempfile import TemporaryDirectory
from typing import Optional

from genie_common.tools.logs import logger
from spotipyio import SpotifyClient

from server.consts.app_consts import PLAYLIST_DETAILS, ACCESS_CODE
from server.data.playlist_creation_config import PlaylistCreationConfig
from server.data.playlist_creation_context import PlaylistCreationContext
from server.data.playlist_resources import PlaylistResources


class BaseContentController(ABC):
    def __init__(self, context: PlaylistCreationContext):
        self._context = context

    async def post(self, request_body: dict, case_id: str) -> None:
        logger.info("Received request", extra={"controller": self.__class__.__name__})
        access_code = request_body[ACCESS_CODE]

        with TemporaryDirectory() as dir_path:
            async with self._context.session_creator.create(access_code) as spotify_session:
                spotify_client = SpotifyClient.create(spotify_session)

                await self._execute_playlist_creation_process(
                    request_body=request_body,
                    dir_path=dir_path,
                    spotify_client=spotify_client,
                    case_id=case_id
                )

    async def _execute_playlist_creation_process(self,
                                                 request_body: dict,
                                                 dir_path: str,
                                                 spotify_client: SpotifyClient,
                                                 case_id: str) -> None:
        logger.info("Starting to execute playlists creation process")
        playlist_id = None
        playlist_resources = await self._generate_playlist_resources(
            case_id=case_id,
            request_body=request_body,
            dir_path=dir_path,
            spotify_client=spotify_client
        )

        if playlist_resources.uris:
            playlist_id = await self._create_playlist(
                request_body=request_body,
                playlist_resources=playlist_resources,
                spotify_client=spotify_client,
                case_id=case_id
            )

        await self._context.cases_manager.mark_completed(case_id=case_id, playlist_id=playlist_id)

    @abstractmethod
    async def _generate_playlist_resources(self,
                                           case_id: str,
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
                               spotify_client: SpotifyClient,
                               case_id: str) -> Optional[str]:
        config = PlaylistCreationConfig(
            spotify_client=spotify_client,
            playlist_details=request_body[PLAYLIST_DETAILS],
            uris=playlist_resources.uris,
        )
        playlist_id = await self._context.playlists_creator.create(case_id, config)

        if playlist_id is not None:
            await self._create_playlist_cover_wrapper(
                request_body=request_body,
                playlist_id=playlist_id,
                config=config,
                image_path=playlist_resources.cover_image_path,
                case_id=case_id
            )
            return playlist_id

    async def _create_playlist_cover_wrapper(self,
                                             request_body: dict,
                                             playlist_id: str,
                                             config: PlaylistCreationConfig,
                                             image_path: str,
                                             case_id: str):
        async with self._context.case_progress_reporter.report(case_id=case_id, status="cover"):
            try:
                await self._create_playlist_cover(
                    request_body=request_body,
                    playlist_id=playlist_id,
                    config=config,
                    image_path=image_path
                )

            except:
                logger.exception('Failed to create playlist cover')

    async def _create_playlist_cover(self,
                                     request_body: dict,
                                     playlist_id: str,
                                     config: PlaylistCreationConfig,
                                     image_path: str) -> None:
        logger.info("Generating playlist cover")
        created_image_path = await self._generate_playlist_cover(request_body, image_path)

        with open(created_image_path, "rb") as f:
            image = f.read()

        logger.info("Updating playlist with generated cover image")
        await config.spotify_client.playlists.update_cover.run(playlist_id, image)
