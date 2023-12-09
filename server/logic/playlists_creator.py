from typing import Optional

from aiohttp import ClientSession
from spotipyio.logic.creators.playlists.playlists_creation_request import PlaylistCreationRequest

from server.consts.api_consts import ID
from server.consts.app_consts import PLAYLIST_NAME, PLAYLIST_DESCRIPTION, IS_PUBLIC
from server.data.playlist_creation_config import PlaylistCreationConfig


class PlaylistsCreator:
    def __init__(self, session: ClientSession):
        self._session = session

    async def create(self, config: PlaylistCreationConfig) -> Optional[str]:
        playlist_id = await self._create_playlist(config)
        if playlist_id is None:
            return

        valid_uris = [uri for uri in config.uris if isinstance(uri, str)]
        await config.spotify_client.playlists.add_items.run(playlist_id=playlist_id, uris=valid_uris)

        return playlist_id

    @staticmethod
    async def _create_playlist(config: PlaylistCreationConfig) -> str:
        user_profile = await config.spotify_client.current_user.profile.run()
        playlist_creation_request = PlaylistCreationRequest(
            user_id=user_profile[ID],
            name=config.playlist_details[PLAYLIST_NAME],
            description=config.playlist_details[PLAYLIST_DESCRIPTION],
            public=config.playlist_details[IS_PUBLIC]
        )
        playlist_creation_response = await config.spotify_client.playlists.create.run(playlist_creation_request)

        return playlist_creation_response[ID]
