from http import HTTPStatus
from random import randint, shuffle
from typing import List, Dict
from unittest.mock import AsyncMock

from _pytest.fixtures import fixture
from genie_common.utils import random_alphanumeric_string, random_string_array, random_integer_array

from server.component_factory import get_request_body_controller
from server.consts.app_consts import REQUEST_BODY
from server.controllers.request_body_controller import RequestBodyController
from server.data.column_details import ColumnDetails
from server.data.column_group import ColumnGroup
from server.data.request_body.playlist_creation_request_body import PlaylistCreationRequestBody
from server.logic.columns_possible_values_querier import ColumnsPossibleValuesQuerier
from server.logic.default_filter_params_generator import DefaultFilterParamsGenerator
from tests.server.integration.test_resources import TestResources


class TestRequestBodyController:
    @fixture(autouse=True, scope="class")
    def set_up(self, resources: TestResources, request_body_controller: RequestBodyController):
        resources.app.dependency_overrides[get_request_body_controller] = lambda: request_body_controller
        yield

    async def test_get(self, resources: TestResources, expected: Dict[str, List[dict]]):
        response = resources.client.get(
            url='api/requestBody',
            auth=resources.auth
        )
        json_response = response.json()
        try:
            assert response.status_code == HTTPStatus.OK.value
            assert json_response == expected
        except Exception as e:
            print(e)

    @fixture(scope="class")
    def min_max_columns(self) -> List[ColumnDetails]:
        n_columns = randint(1, 10)
        return [self._random_column_details(ColumnGroup.MIN_MAX_VALUES) for _ in range(n_columns)]

    @fixture(scope="class")
    def request_body_controller(self,
                                      min_max_columns: List[ColumnDetails],
                                      possible_values_columns: List[ColumnDetails]) -> RequestBodyController:

        columns_details = min_max_columns + possible_values_columns
        shuffle(columns_details)
        possible_values_querier = AsyncMock(ColumnsPossibleValuesQuerier)
        possible_values_querier.query.return_value = columns_details

        return RequestBodyController(
            possible_values_querier=possible_values_querier
        )

    @fixture(scope="class")
    def possible_values_columns(self) -> List[ColumnDetails]:
        n_columns = randint(1, 10)
        return [self._random_column_details(ColumnGroup.POSSIBLE_VALUES) for _ in range(n_columns)]

    @staticmethod
    def _random_column_details(group: ColumnGroup) -> ColumnDetails:
        if group == ColumnGroup.POSSIBLE_VALUES:
            values = random_string_array()
        else:
            values = random_integer_array(length=2)

        return ColumnDetails(
            name=random_alphanumeric_string(),
            values=values,
            group=group,
            description=random_alphanumeric_string()
        )

    @fixture(scope="class")
    def expected(self,
                 min_max_columns: List[ColumnDetails],
                 possible_values_columns: List[ColumnDetails]) -> Dict[str, List[dict]]:
        columns_details = min_max_columns + possible_values_columns
        features_names = {
            "minMaxValues": sorted([col.formatted_name for col in min_max_columns]),
            "possibleValues": sorted([col.formatted_name for col in possible_values_columns]),
        }
        features_values = {
            "minMaxValues": {col.formatted_name: col.values for col in min_max_columns},
            "possibleValues": {col.formatted_name: col.values for col in possible_values_columns}
        }
        features_descriptions = {col.formatted_name: col.description for col in columns_details}
        body = PlaylistCreationRequestBody(
            filter_params=DefaultFilterParamsGenerator().get_filter_params_defaults(columns_details),  # TODO: Write expected without using this class
            features_values=features_values,
            features_names=features_names,
            features_descriptions=features_descriptions
        )

        return {REQUEST_BODY: [body.to_dict()]}
