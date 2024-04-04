from typing import Optional

from aioredis import Redis
from fastapi import FastAPI
from genie_common.utils import random_alphanumeric_string
from genie_datastores.postgres.testing import PostgresMockFactory
from genie_testkit import PostgresTestkit, RedisTestkit
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.testclient import TestClient

from server.application_builder import ApplicationBuilder
from server.component_factory import get_authenticator
from server.middlewares.authentication_middleware import BasicAuthBackend
from server.tools.authenticator import Authenticator


class TestResources:
    def __init__(self,
                 postgres_testkit: PostgresTestkit = PostgresTestkit(),
                 redis_testkit: RedisTestkit = RedisTestkit(),
                 mock_factory: PostgresMockFactory = PostgresMockFactory(),
                 username: str = random_alphanumeric_string(),
                 password: str = random_alphanumeric_string(),
                 client: TestClient = None,
                 engine: Optional[AsyncEngine] = None,
                 redis: Optional[Redis] = None):
        self.postgres_testkit = postgres_testkit
        self.redis_testkit = redis_testkit
        self.mock_factory = mock_factory
        self.username = username
        self.password = password
        self.auth = (username, password)
        self.client = client or self._create_default_test_client()
        self.engine = engine
        self.redis = redis

    def __enter__(self) -> "TestResources":
        self.postgres_testkit.__enter__()
        self.redis_testkit.__enter__()
        self.engine = self.postgres_testkit.get_database_engine()
        self.redis = self.redis_testkit.get_redis()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.engine = None
        self.redis = None
        self.postgres_testkit.__exit__(exc_type, exc_val, exc_tb)
        self.redis_testkit.__exit__(exc_type, exc_val, exc_tb)

    def _create_default_test_client(self) -> TestClient:
        authentication_middleware = Middleware(
            AuthenticationMiddleware,
            backend=BasicAuthBackend(
                username=self.username,
                password=self.password
            )
        )
        app_builder = ApplicationBuilder(middlewares=[authentication_middleware])
        app = app_builder.build()

        return TestClient(app)
