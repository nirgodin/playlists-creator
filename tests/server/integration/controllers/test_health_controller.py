from functools import partial
from http import HTTPStatus

from _pytest.fixtures import fixture
from redis import Redis
from genie_common.utils import random_postgres_connection_url, random_port, random_alphanumeric_string
from genie_datastores.milvus import MilvusClient
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.pool import NullPool

from server.component_factory import get_health_controller
from server.controllers.health_controller import HealthController
from tests.server.integration.test_resources import TestResources


class TestHealthController:
    async def test_check_server_health__is_healthy__returns_200(self, resources):
        resources.app.dependency_overrides[get_health_controller] = partial(
            self._get_health_controller_with_healthy_milvus,
            resources.engine,
            resources.redis,
        )

        response = resources.client.get(url="/health", auth=resources.auth)

        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == {"detail": "Server is healthy"}

    async def test_check_server_health__postgres_unhealthy__returns_503(self,
                                                                        resources: TestResources,
                                                                        non_existing_db_engine: AsyncEngine):
        resources.app.dependency_overrides[get_health_controller] = partial(
            self._get_health_controller_with_healthy_milvus,
            non_existing_db_engine,
            resources.redis
        )

        response = resources.client.get(url="/health", auth=resources.auth)

        assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE.value
        assert response.json() == {"detail": "Could not connect to `Postgres`"}

    async def test_check_server_health__redis_unhealthy__returns_503(self,
                                                                     resources: TestResources,
                                                                     non_existing_redis: Redis):
        resources.app.dependency_overrides[get_health_controller] = partial(
            self._get_health_controller_with_healthy_milvus,
            resources.engine,
            non_existing_redis
        )

        response = resources.client.get(url="/health", auth=resources.auth)

        assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE.value
        assert response.json() == {"detail": "Could not connect to `Redis`"}

    async def test_check_server_health__milvus_unhealthy__returns_503(self,
                                                                      resources: TestResources,
                                                                      non_existing_milvus: MilvusClient):
        resources.app.dependency_overrides[get_health_controller] = lambda: HealthController(
            db_engine=resources.engine,
            redis=resources.redis,
            milvus=non_existing_milvus
        )

        response = resources.client.get(url="/health", auth=resources.auth)

        assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE.value
        assert response.json() == {"detail": "Could not connect to `Milvus`"}

    @staticmethod
    async def _get_health_controller_with_healthy_milvus(db_engine: AsyncEngine, redis: Redis) -> HealthController:
        async with MilvusClient("http://localhost:19530") as milvus:
            yield HealthController(
                db_engine=db_engine,
                redis=redis,
                milvus=milvus
            )

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

    @fixture(scope="class")
    async def non_existing_milvus(self) -> MilvusClient:
        uri = f"http://localhost:{random_port()}"

        async with MilvusClient(uri) as milvus:
            yield milvus
