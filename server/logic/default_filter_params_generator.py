from dataclasses_json.stringcase import camelcase

from server.consts.app_consts import OPERATOR, VALUE, INCLUDE_NAN, GREATER_THAN_OPERATOR, LESS_THAN_OPERATOR
from server.consts.data_consts import IN_OPERATOR
from server.logic.openai.column_details import ColumnDetails
from server.logic.openai.columns_details_creator import ColumnsDetailsCreator
from server.utils.data_utils import load_data


class DefaultFilterParamsGenerator:
    def __init__(self):
        self._data = load_data()
        self._columns_details_creator = ColumnsDetailsCreator()

    def get_filter_params_defaults(self) -> dict:
        filter_params = {}

        for column_details in self._columns_details_creator.get_relevant_columns_details(self._data):
            column_params = self._get_single_column_filter_params(column_details)
            filter_params.update(column_params)

        return filter_params

    def _get_single_column_filter_params(self, column_details: ColumnDetails) -> dict:
        if column_details.operator == IN_OPERATOR:
            return self._get_list_filter_param(column_details.name)

        else:
            return self._get_range_filter_param(column_details)

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
    def _get_range_filter_param(column_details: ColumnDetails) -> dict:
        return {
            camelcase(f'min_{column_details.name}'): {
                OPERATOR: GREATER_THAN_OPERATOR,
                VALUE: column_details.values[0]
            },
            camelcase(f'max_{column_details.name}'): {
                OPERATOR: LESS_THAN_OPERATOR,
                VALUE: column_details.values[1]
            }
        }
