from http import HTTPStatus

from _pytest.fixtures import fixture
from aioredis import Redis
from genie_common.utils import random_postgres_connection_url, random_port, random_alphanumeric_string
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.pool import NullPool

from server.component_factory import get_health_controller
from server.controllers.health_controller import HealthController
from tests.server.integration.test_resources import TestResources


class TestHealthController:
    @fixture(scope="class")
    async def redis(self, resources):
        async with resources.redis_testkit.get_redis() as redis:
            yield redis

    async def test_check_server_health__is_healthy__returns_200(self, resources: TestResources, redis):
        resources.app.dependency_overrides[get_health_controller] = lambda: HealthController(
            db_engine=resources.engine,
            redis=redis
        )

        response = resources.client.get(url="/health", auth=resources.auth)

        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == {"detail": "Server is healthy"}

    async def test_check_server_health__postgres_unhealthy__returns_503(self,
                                                                        resources: TestResources,
                                                                        non_existing_db_engine: AsyncEngine,
                                                                        redis):
        resources.app.dependency_overrides[get_health_controller] = lambda: HealthController(
            db_engine=non_existing_db_engine,
            redis=redis
        )

        response = resources.client.get(url="/health", auth=resources.auth)

        assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE.value
        assert response.json() == {"detail": "Could not connect to `Postgres`"}

    async def test_check_server_health__redis_unhealthy__returns_503(self,
                                                                     resources: TestResources,
                                                                     non_existing_redis: Redis):
        resources.app.dependency_overrides[get_health_controller] = lambda: HealthController(
            db_engine=resources.engine,
            redis=non_existing_redis
        )

        response = resources.client.get(url="/health", auth=resources.auth)

        assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE.value
        assert response.json() == {"detail": "Could not connect to `Redis`"}

    @fixture(scope="class")
    def non_existing_db_engine(self) -> AsyncEngine:
        url = random_postgres_connection_url()
        return create_async_engine(url=url, poolclass=NullPool)

    @fixture(scope="class")
    def non_existing_redis(self) -> Redis:
        return Redis(
            host=random_alphanumeric_string(),
            port=random_port(),
            password=random_alphanumeric_string(),
        )
