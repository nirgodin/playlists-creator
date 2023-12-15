from typing import List

from dataclasses_json.stringcase import camelcase

from server.consts.app_consts import OPERATOR, VALUE, INCLUDE_NAN, GREATER_THAN_OPERATOR, LESS_THAN_OPERATOR
from server.consts.data_consts import IN_OPERATOR
from server.data.column_group import ColumnGroup
from server.data.column_details import ColumnDetails


class DefaultFilterParamsGenerator:
    def get_filter_params_defaults(self, columns_values: List[ColumnDetails]) -> dict:
        filter_params = {}

        for column in columns_values:
            column_params = self._get_single_column_filter_params(column)
            filter_params.update(column_params)

        return filter_params

    def _get_single_column_filter_params(self, column: ColumnDetails) -> dict:
        if column.group == ColumnGroup.POSSIBLE_VALUES:
            return self._get_list_filter_param(column.name)

        return self._get_range_filter_param(column)

    @staticmethod
    def _get_list_filter_param(column_name: str) -> dict:
        return {
            camelcase(column_name): {
                OPERATOR: IN_OPERATOR,
                VALUE: [],
                INCLUDE_NAN: True
            }
        }

    @staticmethod
    def _get_range_filter_param(column: ColumnDetails) -> dict:
        return {
            camelcase(f'min_{column.name}'): {
                OPERATOR: GREATER_THAN_OPERATOR,
                VALUE: column.values[0]
            },
            camelcase(f'max_{column.name}'): {
                OPERATOR: LESS_THAN_OPERATOR,
                VALUE: column.values[1]
            }
        }
