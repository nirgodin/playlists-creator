from datetime import timedelta
from typing import Dict

from genie_common.encoders import GzipJsonEncoder
from genie_datastores.redis import RedisClient
from spotipyio import AccessTokenGenerator
from spotipyio.logic.authentication.spotify_grant_type import SpotifyGrantType

from server.consts.app_consts import ACCESS_CODE_CACHE_TTL


class CachedTokenGenerator:
    def __init__(self, access_token_generator: AccessTokenGenerator):
        self._access_token_generator = access_token_generator

    @RedisClient.cache(encoder=GzipJsonEncoder(), ttl=timedelta(minutes=ACCESS_CODE_CACHE_TTL))
    async def generate(self, grant_type: SpotifyGrantType, access_code: str) -> Dict[str, str]:
        return await self._access_token_generator.generate(grant_type, access_code)
