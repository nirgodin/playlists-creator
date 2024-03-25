from _pytest.fixtures import fixture

from server.logic.database_client import DatabaseClient
from server.utils.data_utils import get_possible_values_columns, get_orm_conditions_map
from tests.server.integration.test_resources import TestResources


@fixture(scope="session")
def resources() -> TestResources:
    with TestResources() as test_resources:
        yield test_resources


@fixture(scope="session")
def db_client(resources: TestResources) -> DatabaseClient:
    return DatabaseClient(
        db_engine=resources.engine,
        columns=get_possible_values_columns(),
        orm_conditions_map=get_orm_conditions_map()
    )
