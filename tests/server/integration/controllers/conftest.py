from _pytest.fixtures import fixture

from server.logic.cases_manager import CasesManager
from server.tools.case_progress_reporter import CaseProgressReporter
from tests.server.integration.test_resources import TestResources


@fixture(scope="session")
def cases_manager(resources: TestResources, case_progress_reporter: CaseProgressReporter) -> CasesManager:
    return CasesManager(
        db_engine=resources.engine,
        case_progress_reporter=case_progress_reporter
    )


@fixture(scope="session")
def case_progress_reporter(resources: TestResources) -> CaseProgressReporter:
    return CaseProgressReporter(resources.engine)
