from typing import Optional

from aiohttp import ClientSession
from genie_common.tools import logger
from spotipyio.logic.creators.playlists.playlists_creation_request import PlaylistCreationRequest

from server.consts.api_consts import ID
from server.consts.app_consts import PLAYLIST_NAME, PLAYLIST_DESCRIPTION, IS_PUBLIC
from server.data.case_status import CaseStatus
from server.data.playlist_creation_config import PlaylistCreationConfig
from server.tools.case_progress_reporter import CaseProgressReporter


class PlaylistsCreator:
    def __init__(self, session: ClientSession, case_progress_reporter: CaseProgressReporter):
        self._session = session
        self._case_progress_reporter = case_progress_reporter

    async def create(self, case_id: str, config: PlaylistCreationConfig) -> Optional[str]:
        async with self._case_progress_reporter.report(case_id=case_id, status=CaseStatus.PLAYLIST):
            return await self._create_playlist(config)

    async def _create_playlist(self, config: PlaylistCreationConfig) -> Optional[str]:
        playlist_id = await self._create_empty_playlist(config)
        if playlist_id is None:
            return

        logger.info("Adding playlist items")
        valid_uris = [uri for uri in config.uris if isinstance(uri, str)]
        await config.spotify_client.playlists.add_items.run(playlist_id=playlist_id, uris=valid_uris)

        return playlist_id

    @staticmethod
    async def _create_empty_playlist(config: PlaylistCreationConfig) -> str:
        logger.info("Creating empty playlist")
        user_profile = await config.spotify_client.current_user.profile.run()
        playlist_creation_request = PlaylistCreationRequest(
            user_id=user_profile[ID],
            name=config.playlist_details[PLAYLIST_NAME],
            description=config.playlist_details[PLAYLIST_DESCRIPTION],
            public=config.playlist_details[IS_PUBLIC]
        )
        playlist_creation_response = await config.spotify_client.playlists.create.run(playlist_creation_request)

        return playlist_creation_response[ID]
