from typing import Optional

from aioredis import Redis
from genie_common.utils import random_alphanumeric_string
from genie_datastores.postgres.testing import PostgresMockFactory
from genie_testkit import PostgresTestkit, RedisTestkit
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.testclient import TestClient

from main import app
from server.component_factory import get_authenticator
from server.tools.authenticator import Authenticator


class TestResources:
    def __init__(self,
                 client: TestClient = TestClient(app),
                 postgres_testkit: PostgresTestkit = PostgresTestkit(),
                 redis_testkit: RedisTestkit = RedisTestkit(),
                 mock_factory: PostgresMockFactory = PostgresMockFactory(),
                 username: str = random_alphanumeric_string(),
                 password: str = random_alphanumeric_string(),
                 engine: Optional[AsyncEngine] = None,
                 redis: Optional[Redis] = None):
        self.client = client
        self.postgres_testkit = postgres_testkit
        self.redis_testkit = redis_testkit
        self.mock_factory = mock_factory
        self.username = username
        self.password = password
        self.auth = (username, password)
        self.engine = engine
        self.redis = redis

    def __enter__(self) -> "TestResources":
        self.postgres_testkit.__enter__()
        self.redis_testkit.__enter__()
        self.engine = self.postgres_testkit.get_database_engine()
        self.redis = self.redis_testkit.get_redis()
        app.dependency_overrides[get_authenticator] = lambda: Authenticator(
            username=self.username,
            password=self.password
        )

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.engine = None
        self.redis = None
        self.postgres_testkit.__exit__(exc_type, exc_val, exc_tb)
        self.redis_testkit.__exit__(exc_type, exc_val, exc_tb)
