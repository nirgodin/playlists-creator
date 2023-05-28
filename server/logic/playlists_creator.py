from typing import List, Dict, Optional

import requests

from server.consts.api_consts import CREATE_PLAYLIST_URL_FORMAT, ADD_PLAYLIST_ITEMS_URL_FORMAT, USER_PROFILE_URL, ID, \
    NAME, DESCRIPTION, PUBLIC, REFRESH_TOKEN
from server.consts.app_consts import PLAYLIST_NAME, PLAYLIST_DESCRIPTION, IS_PUBLIC
from server.data.playlist_creation_config import PlaylistCreationConfig


class PlaylistsCreator:
    def create(self, config: PlaylistCreationConfig, retries_left: int) -> Optional[str]:
        playlist_id = self._create_playlist_wrapper(config, retries_left)

        if playlist_id is None:
            return

        valid_uris = [uri for uri in config.uris if isinstance(uri, str)]
        self._add_playlist_items(playlist_id, valid_uris, config.headers)

        return playlist_id

    def _create_playlist_wrapper(self, config: PlaylistCreationConfig, retries_left: int) -> Optional[str]:
        if retries_left == 0:
            return

        try:
            return self._create_playlist(config)

        except:
            config.access_code = config.access_token_generator_response[REFRESH_TOKEN]
            return self._create_playlist_wrapper(config, retries_left=retries_left - 1)

    def _create_playlist(self, config: PlaylistCreationConfig) -> str:
        user_id = self._fetch_user_id(config.headers)
        url = CREATE_PLAYLIST_URL_FORMAT.format(user_id)
        body = {
            NAME: config.playlist_details[PLAYLIST_NAME],
            DESCRIPTION: config.playlist_details[PLAYLIST_DESCRIPTION],
            PUBLIC: config.playlist_details[IS_PUBLIC]
        }
        raw_response = requests.post(url=url, json=body, headers=config.headers)
        response = raw_response.json()

        return response[ID]

    @staticmethod
    def _fetch_user_id(headers: dict) -> str:
        response = requests.get(url=USER_PROFILE_URL, headers=headers).json()
        return response[ID]

    @staticmethod
    def _add_playlist_items(playlist_id: str, uris: List[str], headers: dict) -> None:
        url = ADD_PLAYLIST_ITEMS_URL_FORMAT.format(playlist_id)
        body = {
            'uris': uris
        }
        raw_response = requests.post(url=url, json=body, headers=headers)
        response = raw_response.json()
