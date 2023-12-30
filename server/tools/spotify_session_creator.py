import asyncio
import os
from contextlib import asynccontextmanager
from datetime import timedelta

from genie_common.encoders import GzipJsonEncoder
from genie_common.utils import build_authorization_headers, create_client_session
from genie_datastores.redis import RedisClient
from spotipyio import AccessTokenGenerator
from spotipyio.consts.api_consts import ACCESS_TOKEN
from spotipyio.logic.authentication.spotify_grant_type import SpotifyGrantType
from spotipyio.logic.authentication.spotify_session import SpotifySession

from server.consts.env_consts import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI


class SpotifySessionCreator:
    def __init__(self, token_generator: AccessTokenGenerator):
        self._token_generator = token_generator

    @asynccontextmanager
    async def create(self, access_code: str) -> SpotifySession:
        session = None

        try:
            session = await self._build_session(access_code)
            yield session

        finally:
            if session is not None:
                await session.__aexit__(None, None, None)

    async def _build_session(self, access_code: str) -> SpotifySession:
        response = await self._fetch(SpotifyGrantType.AUTHORIZATION_CODE, access_code)
        access_token = response[ACCESS_TOKEN]
        headers = build_authorization_headers(access_token)
        raw_session = create_client_session(headers)
        client_session = await raw_session.__aenter__()

        return SpotifySession(session=client_session)

    @RedisClient.cache(encoder=GzipJsonEncoder(), ttl=timedelta(minutes=1))  # TODO: Transform to configurable env var
    async def _fetch(self, grant_type: SpotifyGrantType, access_code: str) -> dict:
        async with self._token_generator as token_generator:
            return await token_generator.generate(grant_type, access_code)
