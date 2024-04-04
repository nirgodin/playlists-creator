from http import HTTPStatus
from random import randint

import pytest
from _pytest.fixtures import fixture
from genie_common.utils import random_alphanumeric_string
from genie_datastores.postgres.models import Case
from genie_datastores.postgres.operations import insert_records
from genie_datastores.postgres.testing import postgres_session

from server.component_factory import get_cases_controller
from server.consts.app_consts import MESSAGE
from server.consts.cases_consts import PLAYLIST_ID, CASE_STATUS, CASE_FAILURE_MESSAGE_FORMAT
from server.controllers.case_controller import CasesController
from server.logic.cases_manager import CasesManager
from tests.server.integration.test_resources import TestResources


class TestCaseController:
    @fixture(autouse=True, scope="class")
    async def set_up(self, resources: TestResources, cases_controller: CasesController, case: Case):
        resources.app.dependency_overrides[get_cases_controller] = lambda: cases_controller
        async with postgres_session(resources.engine):
            await insert_records(engine=resources.engine, records=[case])

            yield

    async def test_get_playlist(self, resources: TestResources, case: Case, case_id: str):
        response = resources.client.get(
            url=f'api/cases/{case_id}/playlist',
            auth=resources.auth
        )

        assert response.status_code == HTTPStatus.OK.value
        assert response.json() == {PLAYLIST_ID: case.playlist_id}

    async def test_get_status__returns_last_case_inserter(self, resources: TestResources, case_id: str):
        n_cases = randint(1, 5)
        progress_records = [resources.mock_factory.case_progress(case_id=case_id) for _ in range(n_cases)]

        for record in progress_records:
            await insert_records(engine=resources.engine, records=[record])

            response = resources.client.get(
                url=f'api/cases/{case_id}/progress',
                auth=resources.auth
            )

            assert response.status_code == HTTPStatus.OK.value
            assert response.json() == {CASE_STATUS: record.status}

    @pytest.mark.parametrize("route", ["progress", "playlist"])
    async def test_missing_case__returns_400_response(self, route: str, resources: TestResources):
        missing_case_id = random_alphanumeric_string()
        expected_response = {MESSAGE: CASE_FAILURE_MESSAGE_FORMAT.format(case_id=missing_case_id)}

        response = resources.client.get(
            url=f'api/cases/{missing_case_id}/{route}',
            auth=resources.auth
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST.value
        assert response.json() == expected_response

    @fixture(scope="class")
    def cases_controller(self, cases_manager: CasesManager) -> CasesController:
        return CasesController(cases_manager)

    @fixture(scope="class")
    def case_id(self) -> str:
        return random_alphanumeric_string()

    @fixture(scope="class")
    def case(self, resources: TestResources, case_id: str) -> Case:
        return resources.mock_factory.case(id=case_id)
