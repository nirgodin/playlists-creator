from random import randint
from typing import Dict
from unittest.mock import AsyncMock, patch

from _pytest.fixtures import fixture
from redis import Redis
from genie_common.encoders import GzipJsonEncoder
from genie_common.utils import random_alphanumeric_string, random_string_array
from spotipyio.auth import SpotifyGrantType
from spotipyio.logic.authorization import AccessTokenGenerator

from server.tools.cached_token_generator import CachedTokenGenerator
from tests.server.integration.test_resources import TestResources


class TestCachedTokenGenerator:
    @fixture(autouse=True, scope="class")
    def set_up(self, resources: TestResources) -> None:
        with patch("genie_datastores.redis.redis_client.get_redis") as mock_get_redis:
            mock_get_redis.return_value = resources.redis
            yield

    async def test_generate__no_cache__calls_spotify_and_sets_key(self,
                                                                  token_generator: CachedTokenGenerator,
                                                                  access_token_generator: AsyncMock,
                                                                  resources: TestResources,
                                                                  encoder: GzipJsonEncoder,
                                                                  response: Dict[str, str]):
        access_code = random_alphanumeric_string()

        actual = await token_generator.generate(SpotifyGrantType.AUTHORIZATION_CODE, access_code)

        assert actual == response
        assert access_token_generator.generate.call_count == 1
        self._assert_key_stored_in_cache(
            redis=resources.redis,
            encoder=encoder,
            access_code=access_code,
            response=response
        )

    async def test_create__with_cache__doesnt_call_spotify(self,
                                                           resources: TestResources,
                                                           encoder: GzipJsonEncoder,
                                                           response: Dict[str, str],
                                                           token_generator: CachedTokenGenerator,
                                                           access_token_generator: AsyncMock):
        access_code = self._given_cached_access_code(resources.redis, encoder, response)

        actual = await token_generator.generate(SpotifyGrantType.AUTHORIZATION_CODE, access_code)

        assert actual == response
        assert access_token_generator.generate.call_count == 0

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
            "access_token": random_alphanumeric_string(),
            "token_type": random_alphanumeric_string(),
            "scope": " ".join(scopes),
            "expires_in": randint(0, 3000),
            "refresh_token": random_alphanumeric_string(),
        }

    @fixture(scope="function")
    def access_token_generator(self, response: Dict[str, str]) -> AsyncMock:
        mock_token_generator = AsyncMock(AccessTokenGenerator)
        mock_token_generator.generate.return_value = response

        yield mock_token_generator

        mock_token_generator.reset_mock()

    @staticmethod
    def _assert_key_stored_in_cache(redis: Redis,
                                    encoder: GzipJsonEncoder,
                                    access_code: str,
                                    response: Dict[str, str]) -> None:
        cache_response = redis.get(access_code)
        decoded_response = encoder.decode(cache_response)
        assert decoded_response == response

    @staticmethod
    def _given_cached_access_code(redis: Redis, encoder: GzipJsonEncoder, response: Dict[str, str]) -> str:
        access_code = random_alphanumeric_string()
        encoded_response = encoder.encode(response)
        redis.set(access_code, encoded_response)

        return access_code
