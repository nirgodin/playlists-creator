from typing import List, Optional

from aiohttp import ClientSession

from server.consts.api_consts import CREATE_PLAYLIST_URL_FORMAT, ADD_PLAYLIST_ITEMS_URL_FORMAT, USER_PROFILE_URL, ID, \
    NAME, DESCRIPTION, PUBLIC, REFRESH_TOKEN
from server.consts.app_consts import PLAYLIST_NAME, PLAYLIST_DESCRIPTION, IS_PUBLIC
from server.data.playlist_creation_config import PlaylistCreationConfig


class PlaylistsCreator:
    def __init__(self, session: ClientSession):
        self._session = session

    async def create(self, config: PlaylistCreationConfig, retries_left: int) -> Optional[str]:
        playlist_id = await self._create_playlist_wrapper(config, retries_left)

        if playlist_id is None:
            return

        valid_uris = [uri for uri in config.uris if isinstance(uri, str)]
        await self._add_playlist_items(playlist_id, valid_uris, config.headers)

        return playlist_id

    async def _create_playlist_wrapper(self, config: PlaylistCreationConfig, retries_left: int) -> Optional[str]:
        if retries_left == 0:
            return

        try:
            return await self._create_playlist(config)

        except:
            config.access_code = config.access_token_generator_response[REFRESH_TOKEN]
            return await self._create_playlist_wrapper(config, retries_left=retries_left - 1)

    async def _create_playlist(self, config: PlaylistCreationConfig) -> str:
        try:
            user_id = await self._fetch_user_id(config.headers)
        except Exception as e:
            print('b')
        url = CREATE_PLAYLIST_URL_FORMAT.format(user_id)
        body = {
            NAME: config.playlist_details[PLAYLIST_NAME],
            DESCRIPTION: config.playlist_details[PLAYLIST_DESCRIPTION],
            PUBLIC: config.playlist_details[IS_PUBLIC]
        }

        async with self._session.post(url=url, json=body, headers=config.headers) as raw_response:
            # raw_response.raise_for_status()
            response = await raw_response.json()

        return response[ID]

    async def _fetch_user_id(self, headers: dict) -> str:
        async with self._session.get(url=USER_PROFILE_URL, headers=headers) as raw_response:
            # raw_response.raise_for_status()
            response = await raw_response.json()

        return response[ID]

    async def _add_playlist_items(self, playlist_id: str, uris: List[str], headers: dict) -> None:
        url = ADD_PLAYLIST_ITEMS_URL_FORMAT.format(playlist_id)
        body = {
            'uris': uris
        }

        async with self._session.post(url=url, json=body, headers=headers) as raw_response:
            raw_response.raise_for_status()
            response = await raw_response.json()
