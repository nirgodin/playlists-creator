from random import randint, shuffle
from typing import Dict, Any, List, Union

from _pytest.fixtures import fixture
from genie_common.utils import merge_dicts, random_lowercase_string, random_string_array

from server.consts.app_consts import FILTER_PARAMS
from server.data.query_condition import QueryCondition
from server.logic.parameters_transformer import ParametersTransformer


class TestParametersTransformer:
    def test_transform(self, request_body: dict, expected: List[QueryCondition]):
        transformer = ParametersTransformer()
        actual = transformer.transform(request_body)
        assert sorted(actual, key=lambda x: x.column) == sorted(expected, key=lambda x: x.column)

    @fixture(scope="class")
    def request_body(self, filter_params: Dict[str, Dict[str, Any]]) -> dict:
        return {
            FILTER_PARAMS: filter_params
        }

    @fixture(scope="class")
    def filter_params(self,
                      greater_than_columns: Dict[str, float],
                      lower_than_columns: Dict[str, float],
                      contained_columns: Dict[str, List[str]]) -> Dict[str, Dict[str, float]]:
        greater_params = [self._to_filter_param(column, value, ">=") for column, value in greater_than_columns.items()]
        lower_params = [self._to_filter_param(column, value, "<=") for column, value in lower_than_columns.items()]
        contained_params = [self._to_filter_param(column, value, "in") for column, value in contained_columns.items()]
        params = greater_params + lower_params + contained_params
        shuffle(params)

        return merge_dicts(*params)

    @fixture(scope="class")
    def greater_than_columns(self) -> Dict[str, float]:
        n_params = randint(0, 5)
        return {random_lowercase_string(): randint(0, 100) for _ in range(n_params)}

    @fixture(scope="class")
    def lower_than_columns(self) -> Dict[str, float]:
        n_params = randint(0, 5)
        return {random_lowercase_string(): randint(0, 100) for _ in range(n_params)}

    @fixture(scope="class")
    def contained_columns(self) -> Dict[str, List[str]]:
        n_params = randint(0, 5)
        return {random_lowercase_string(): random_string_array() for _ in range(n_params)}

    @fixture(scope="class")
    def expected(self,
                 greater_than_columns: Dict[str, float],
                 lower_than_columns: Dict[str, float],
                 contained_columns: Dict[str, List[str]]) -> List[QueryCondition]:
        greater_than_conditions = self._to_query_conditions(greater_than_columns, ">=")
        lower_than_conditions = self._to_query_conditions(lower_than_columns, "<=")
        contained_conditions = self._to_query_conditions(lower_than_columns, "in")

        return greater_than_conditions + lower_than_conditions + contained_conditions

    @staticmethod
    def _to_filter_param(column_name: str, value: Union[float, List[str]], operator: str) -> Dict[str, Dict[str, float]]:
        column_name = f"min{column_name.capitalize()}"
        return {
            column_name: {
                "operator": operator,
                "value": value
            }
        }

    @staticmethod
    def _to_query_conditions(column_values: Dict[str, Any], operator: str) -> List[QueryCondition]:
        return [
            QueryCondition(column=column, operator=operator, value=value) for column, value in column_values.items()
        ]
