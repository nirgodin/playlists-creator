from typing import List, Dict

from dataclasses_json.stringcase import camelcase

from server.consts.app_consts import GREATER_THAN_OPERATOR, LESS_THAN_OPERATOR
from server.consts.data_consts import IN_OPERATOR
from server.data.column_details import ColumnDetails
from server.data.column_group import ColumnGroup
from server.data.request_body.filter_param import FilterParam


class DefaultFilterParamsGenerator:
    def get_filter_params_defaults(self, columns_values: List[ColumnDetails]) -> Dict[str, FilterParam]:
        filter_params = {}

        for column in columns_values:
            column_params = self._get_single_column_filter_params(column)
            filter_params.update(column_params)

        return filter_params

    def _get_single_column_filter_params(self, column: ColumnDetails) -> Dict[str, FilterParam]:
        if column.group == ColumnGroup.POSSIBLE_VALUES:
            return self._get_list_filter_param(column.name)

        return self._get_range_filter_param(column)

    @staticmethod
    def _get_list_filter_param(column_name: str) -> Dict[str, FilterParam]:
        return {
            camelcase(column_name): FilterParam(
                operator=IN_OPERATOR,
                value=[]
            )
        }

    @staticmethod
    def _get_range_filter_param(column: ColumnDetails) -> Dict[str, FilterParam]:
        return {
            camelcase(f'min_{column.name}'): FilterParam(
                operator=GREATER_THAN_OPERATOR,
                value=column.values[0]
            ),
            camelcase(f'max_{column.name}'): FilterParam(
                operator=LESS_THAN_OPERATOR,
                value=column.values[1]
            )
        }
