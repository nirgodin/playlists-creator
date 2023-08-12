import base64
import os
from typing import Dict, Optional

from aiohttp import ClientSession
from async_lru import alru_cache

from server.consts.api_consts import TOKEN_REQUEST_URL, REDIRECT_URI, CODE, GRANT_TYPE, JSON, REFRESH_TOKEN, CLIENT_ID
from server.consts.env_consts import SPOTIPY_CLIENT_SECRET, SPOTIPY_CLIENT_ID, SPOTIPY_REDIRECT_URI
from server.data.spotify_grant_type import SpotifyGrantType


class AccessTokenGenerator:
    def __init__(self, session: ClientSession):
        self._session = session

    @alru_cache
    async def generate(self, grant_type: SpotifyGrantType, access_code: Optional[str] = None) -> Optional[Dict[str, str]]:
        encoded_header = self._get_encoded_header()
        headers = {'Authorization': f"Basic {encoded_header}"}
        data = self._build_request_payload(access_code, grant_type)

        async with self._session.post(url=TOKEN_REQUEST_URL, headers=headers, data=data) as raw_response:
            if raw_response.status == 200:
                return await raw_response.json()

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
