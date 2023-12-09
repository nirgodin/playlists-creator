from aiohttp import ClientSession
from genie_common.utils import build_authorization_headers

from server.consts.api_consts import ACCESS_TOKEN
from server.consts.data_consts import ITEMS, URI
from spotipyio.logic.authentication.spotify_grant_type import SpotifyGrantType
from server.logic.access_token_generator import AccessTokenGenerator

TOP_USER_PLAYS_URL_FORMAT = "https://api.spotify.com/v1/me/top/{type}"


class WrappedTracksCollector:
    def __init__(self, session: ClientSession, access_token_generator: AccessTokenGenerator):
        self._session = session
        self._access_token_generator = access_token_generator

    async def collect(self, access_code: str):
        access_token_generator_response = await self._access_token_generator.generate(
            grant_type=SpotifyGrantType.AUTHORIZATION_CODE,
            access_code=access_code
        )
        bearer_token = access_token_generator_response.get(ACCESS_TOKEN)
        headers = build_authorization_headers(bearer_token)
        url = TOP_USER_PLAYS_URL_FORMAT.format(type="tracks")
        params = {
            "time_range": "long_term",
            "limit": 50,
            "offset": 0
        }

        async with self._session.get(url=url, params=params, headers=headers) as raw_response:
            res = await raw_response.json()

        return [item[URI] for item in res[ITEMS]]
