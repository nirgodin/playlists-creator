import base64
import os
from functools import lru_cache
from typing import Dict, Optional

import requests

from server.consts.api_consts import TOKEN_REQUEST_URL, REDIRECT_URI, CODE, GRANT_TYPE, JSON, REFRESH_TOKEN, CLIENT_ID
from server.consts.env_consts import SPOTIPY_CLIENT_SECRET, SPOTIPY_CLIENT_ID, SPOTIPY_REDIRECT_URI
from server.data.spotify_grant_type import SpotifyGrantType


class AccessTokenGenerator:
    @staticmethod
    @lru_cache
    def generate(grant_type: SpotifyGrantType, access_code: Optional[str] = None) -> Optional[Dict[str, str]]:
        encoded_header = AccessTokenGenerator._get_encoded_header()
        headers = {'Authorization': f"Basic {encoded_header}"}
        data = AccessTokenGenerator._build_request_payload(access_code, grant_type)
        response = requests.post(
            url=TOKEN_REQUEST_URL,
            headers=headers,
            data=data
        )

        if response.status_code == 200:
            return response.json()

    @staticmethod
    def _get_encoded_header() -> str:
        client_id = os.environ[SPOTIPY_CLIENT_ID]
        client_secret = os.environ[SPOTIPY_CLIENT_SECRET]
        bytes_auth = bytes(f"{client_id}:{client_secret}", "ISO-8859-1")
        b64_auth = base64.b64encode(bytes_auth)

        return b64_auth.decode('ascii')

    @staticmethod
    def _build_request_payload(access_code: str, grant_type: SpotifyGrantType) -> Dict[str, str]:
        if grant_type == SpotifyGrantType.AUTHORIZATION_CODE:
            return {
                GRANT_TYPE: grant_type.value,
                CODE: access_code,
                REDIRECT_URI: os.environ[SPOTIPY_REDIRECT_URI],
                JSON: True
            }

        elif grant_type == SpotifyGrantType.REFRESH_TOKEN:
            return {
                GRANT_TYPE: grant_type.value,
                REFRESH_TOKEN: access_code,
                CLIENT_ID: os.environ[SPOTIPY_CLIENT_ID]
            }

        elif grant_type == SpotifyGrantType.CLIENT_CREDENTIALS:
            return {
                GRANT_TYPE: grant_type.value,
                JSON: True
            }

        else:
            raise ValueError('Did not recognize grant type')
