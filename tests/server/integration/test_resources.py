from typing import Optional

from fastapi import FastAPI
from genie_common.utils import random_alphanumeric_string
from genie_datastores.milvus import MilvusClient
from genie_datastores.postgres.testing import PostgresMockFactory
from genie_testkit import PostgresTestkit, RedisTestkit, MilvusTestkit
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.testclient import TestClient

from server.application_builder import ApplicationBuilder
from server.component_factory import get_authentication_middleware


class TestResources:
    def __init__(self,
                 postgres_testkit: PostgresTestkit = PostgresTestkit(),
                 redis_testkit: RedisTestkit = RedisTestkit(),
                 milvus_testkit: MilvusTestkit = MilvusTestkit(),
                 mock_factory: PostgresMockFactory = PostgresMockFactory(),
                 username: str = random_alphanumeric_string(),
                 password: str = random_alphanumeric_string(),
                 app: Optional[FastAPI] = None,
                 engine: Optional[AsyncEngine] = None,
                 redis: Optional[Redis] = None,
                 milvus: Optional[MilvusClient] = None):
        self.postgres_testkit = postgres_testkit
        self.redis_testkit = redis_testkit
        self.milvus_testkit = milvus_testkit
        self.mock_factory = mock_factory
        self.username = username
        self.password = password
        self.auth = (username, password)
        self.app = app or self._create_default_app()
        self.client = TestClient(self.app)
        self.engine = engine
        self.redis = redis
        self.milvus = milvus

    async def __aenter__(self) -> "TestResources":
        self.postgres_testkit.__enter__()
        self.redis_testkit.__enter__()
        # self.milvus_testkit.__enter__()
        self.engine = self.postgres_testkit.get_database_engine()
        self.redis = self.redis_testkit.get_redis()
        # self.milvus = await MilvusClient(self.milvus_testkit.uri).__aenter__()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.engine = None
        self.postgres_testkit.__exit__(exc_type, exc_val, exc_tb)
        self.redis = None
        self.redis_testkit.__exit__(exc_type, exc_val, exc_tb)
        # await self.milvus.__aexit__(exc_type, exc_val, exc_tb)
        self.milvus = None
        # self.milvus_testkit.__exit__(exc_type, exc_val, exc_tb)

    def _create_default_app(self) -> FastAPI:
        authentication_middleware = get_authentication_middleware(self.username, self.password)
        app_builder = ApplicationBuilder(middlewares=[authentication_middleware])
        return app_builder.build()
