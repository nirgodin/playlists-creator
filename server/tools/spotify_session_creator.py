from contextlib import asynccontextmanager

from genie_common.clients.utils import build_authorization_headers, create_client_session
from spotipyio import SpotifySession
from spotipyio.auth import SpotifyGrantType

from server.tools.cached_token_generator import CachedTokenGenerator


class SpotifySessionCreator:
    def __init__(self, token_generator: CachedTokenGenerator):
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
        response = await self._token_generator.generate(SpotifyGrantType.AUTHORIZATION_CODE, access_code)
        access_token = response["access_token"]
        headers = build_authorization_headers(access_token)
        raw_session = create_client_session(headers)
        client_session = await raw_session.__aenter__()

        return SpotifySession(session=client_session)
