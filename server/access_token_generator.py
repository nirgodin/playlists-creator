import base64
import os
from typing import Dict

import requests

from server.logic.consts.api_consts import TOKEN_REQUEST_URL, REDIRECT_URI, CODE, GRANT_TYPE, JSON, ACCESS_TOKEN
from server.logic.consts.env_consts import SPOTIPY_CLIENT_SECRET, SPOTIPY_CLIENT_ID, SPOTIPY_REDIRECT_URI
from server.spotify_grant_type import SpotifyGrantType


class AccessTokenGenerator:
    @staticmethod
    def generate(access_code: str) -> str:
        encoded_header = AccessTokenGenerator._get_encoded_header()
        headers = {'Authorization': f"Basic {encoded_header}"}
        data = AccessTokenGenerator._build_request_payload(access_code)
        response = requests.post(
            url=TOKEN_REQUEST_URL,
            headers=headers,
            data=data
        ).json()

        return response[ACCESS_TOKEN]

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
