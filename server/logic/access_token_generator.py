import base64
import os
from functools import lru_cache
from typing import Dict, Optional

import requests

from server.consts.api_consts import TOKEN_REQUEST_URL, REDIRECT_URI, CODE, GRANT_TYPE, JSON, ACCESS_TOKEN
from server.consts.env_consts import SPOTIPY_CLIENT_SECRET, SPOTIPY_CLIENT_ID, SPOTIPY_REDIRECT_URI
from server.data.spotify_grant_type import SpotifyGrantType


class AccessTokenGenerator:
    @staticmethod
    @lru_cache
    def generate(access_code: str) -> Optional[Dict[str, str]]:
        encoded_header = AccessTokenGenerator._get_encoded_header()
        headers = {'Authorization': f"Basic {encoded_header}"}
        data = AccessTokenGenerator._build_request_payload(access_code)
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
    def _build_request_payload(access_code: str) -> Dict[str, str]:
        return {
            GRANT_TYPE: SpotifyGrantType.AUTHORIZATION_CODE.value,
            CODE: access_code,
            REDIRECT_URI: os.environ[SPOTIPY_REDIRECT_URI],
            JSON: True
        }
