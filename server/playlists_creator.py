from typing import List

import requests

from server.utils import build_spotify_headers

CREATE_PLAYLIST_URL_FORMAT = 'https://api.spotify.com/v1/users/{}/playlists'
ADD_PLAYLIST_ITEMS_URL_FORMAT = 'https://api.spotify.com/v1/playlists/{}/tracks'
USER_PROFILE_URL = 'https://api.spotify.com/v1/me'
ID = 'id'


class PlaylistsCreator:
    def create(self, uris: List[str], access_code: str, playlist_details: dict):
        headers = build_spotify_headers(access_code)
        playlist_id = self._create_playlist(playlist_details, headers)
        valid_uris = [uri for uri in uris if isinstance(uri, str)]
        self._add_playlist_items(playlist_id, valid_uris, headers)

    def _create_playlist(self, playlist_details: dict, headers: dict) -> str:
        user_id = self._fetch_user_id(headers)
        url = CREATE_PLAYLIST_URL_FORMAT.format(user_id)
        body = {
            "name": playlist_details['playlistName'],
            "description": playlist_details['playlistDescription'],
            "public": playlist_details['isPublic']
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
