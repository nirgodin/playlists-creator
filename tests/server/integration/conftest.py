from _pytest.fixtures import fixture

from tests.server.integration.test_resources import TestResources


@fixture(scope="session")
def resources() -> TestResources:
    with TestResources() as test_resources:
        yield test_resources
