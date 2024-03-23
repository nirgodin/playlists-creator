from _pytest.fixtures import fixture

from server.logic.database_client import DatabaseClient
from tests.server.integration.test_resources import TestResources


@fixture(scope="session")
def resources() -> TestResources:
    with TestResources() as test_resources:
        yield test_resources


@fixture(scope="session")
def database_client(resources: TestResources) -> DatabaseClient:
    return DatabaseClient(resources.engine)
