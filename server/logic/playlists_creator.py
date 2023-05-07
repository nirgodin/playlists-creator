from typing import List, Dict

import requests

from server.consts.api_consts import CREATE_PLAYLIST_URL_FORMAT, ADD_PLAYLIST_ITEMS_URL_FORMAT, USER_PROFILE_URL, ID, \
    PLAYLIST_LINK_FORMAT, NAME, DESCRIPTION, PUBLIC
from server.consts.app_consts import PLAYLIST_NAME, PLAYLIST_DESCRIPTION, IS_PUBLIC


class PlaylistsCreator:
    def create(self, uris: List[str], headers: Dict[str, str], playlist_details: dict) -> str:
        playlist_id = self._create_playlist(playlist_details, headers)
        valid_uris = [uri for uri in uris if isinstance(uri, str)]
        self._add_playlist_items(playlist_id, valid_uris, headers)
        playlist_link = PLAYLIST_LINK_FORMAT.format(playlist_id)

        return playlist_link

    def _create_playlist(self, playlist_details: dict, headers: dict) -> str:
        user_id = self._fetch_user_id(headers)
        url = CREATE_PLAYLIST_URL_FORMAT.format(user_id)
        body = {
            NAME: playlist_details[PLAYLIST_NAME],
            DESCRIPTION: playlist_details[PLAYLIST_DESCRIPTION],
            PUBLIC: playlist_details[IS_PUBLIC]
        }
        raw_response = requests.post(url=url, json=body, headers=headers)
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
