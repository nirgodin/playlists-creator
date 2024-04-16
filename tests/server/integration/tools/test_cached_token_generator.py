from asyncio import get_running_loop, new_event_loop, AbstractEventLoop
from random import randint
from typing import Dict, Generator
from unittest.mock import AsyncMock, patch

from _pytest.fixtures import fixture
from aioredis import Redis
from genie_common.encoders import GzipJsonEncoder
from genie_common.utils import random_alphanumeric_string, random_string_array
from spotipyio import AccessTokenGenerator
from spotipyio.consts.api_consts import ACCESS_TOKEN, REFRESH_TOKEN
from spotipyio.logic.authentication.spotify_grant_type import SpotifyGrantType

from server.tools.cached_token_generator import CachedTokenGenerator
from tests.server.integration.test_resources import TestResources


class TestCachedTokenGenerator:
    @fixture(autouse=True, scope="class")
    async def set_up(self, redis: Redis) -> None:
        with patch("genie_datastores.redis.redis_client.get_redis") as mock_get_redis:
            mock_get_redis.return_value = redis
            yield

    async def test_generate__no_cache__calls_spotify_and_sets_key(self,
                                                                  redis,
                                                                  token_generator: CachedTokenGenerator,
                                                                  access_token_generator: AsyncMock,
                                                                  resources: TestResources,
                                                                  encoder: GzipJsonEncoder,
                                                                  response: Dict[str, str]):
        access_code = random_alphanumeric_string()

        actual = await token_generator.generate(SpotifyGrantType.AUTHORIZATION_CODE, access_code)

        assert actual == response
        assert access_token_generator.generate.call_count == 1
        await self._assert_key_stored_in_cache(
            redis=redis,
            encoder=encoder,
            access_code=access_code,
            response=response
        )

    async def test_create__with_cache__doesnt_call_spotify(self,
                                                           redis,
                                                           resources: TestResources,
                                                           encoder: GzipJsonEncoder,
                                                           response: Dict[str, str],
                                                           token_generator: CachedTokenGenerator,
                                                           access_token_generator: AsyncMock):
        access_code = await self._given_cached_access_code(redis, encoder, response)

        actual = await token_generator.generate(SpotifyGrantType.AUTHORIZATION_CODE, access_code)

        assert actual == response
        assert access_token_generator.generate.call_count == 0

    @fixture(scope="class")
    async def redis(self, resources: TestResources) -> Redis:
        async with resources.redis_testkit.get_redis() as redis:
            yield redis

    @fixture(scope="class")
    def event_loop(self) -> Generator[AbstractEventLoop, None, None]:
        try:
            loop = get_running_loop()
        except RuntimeError:
            loop = new_event_loop()

        yield loop

        loop.close()

    @fixture(scope="class")
    def encoder(self) -> GzipJsonEncoder:
        return GzipJsonEncoder()

    @fixture(scope="function")
    def token_generator(self, access_token_generator: AsyncMock) -> CachedTokenGenerator:
        return CachedTokenGenerator(access_token_generator)

    @fixture(scope="class")
    def response(self) -> Dict[str, str]:
        scopes = random_string_array()
        return {
            ACCESS_TOKEN: random_alphanumeric_string(),
            "token_type": random_alphanumeric_string(),
            "scope": " ".join(scopes),
            "expires_in": randint(0, 3000),
            REFRESH_TOKEN: random_alphanumeric_string(),
        }

    @fixture(scope="function")
    def access_token_generator(self, response: Dict[str, str]) -> AsyncMock:
        mock_token_generator = AsyncMock(AccessTokenGenerator)
        mock_token_generator.generate.return_value = response

        yield mock_token_generator

        mock_token_generator.reset_mock()

    @staticmethod
    async def _assert_key_stored_in_cache(redis: Redis,
                                          encoder: GzipJsonEncoder,
                                          access_code: str,
                                          response: Dict[str, str]) -> None:
        cache_response = await redis.get(access_code)
        decoded_response = encoder.decode(cache_response)
        assert decoded_response == response

    @staticmethod
    async def _given_cached_access_code(redis: Redis, encoder: GzipJsonEncoder, response: Dict[str, str]) -> str:
        access_code = random_alphanumeric_string()
        encoded_response = encoder.encode(response)
        await redis.set(access_code, encoded_response)

        return access_code
