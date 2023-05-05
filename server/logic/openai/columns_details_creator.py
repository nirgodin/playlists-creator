from functools import lru_cache
from typing import List, Generator

from numpy import dtype
from pandas import DataFrame
from pandas.core.dtypes.common import is_string_dtype, is_bool_dtype

from server.consts.openai_consts import EXCLUDED_COLUMNS, IN_OPERATOR, NUMERIC_OPERATORS, \
    SINGLE_COLUMN_DESCRIPTION_FORMAT
from server.logic.openai.column_details import ColumnDetails
from server.utils import load_data, get_column_possible_values, get_column_min_max_values


class ColumnsDetailsCreator:
    @lru_cache
    def create(self) -> str:
        data = load_data()
        columns_descriptions = []

        for column_details in self.get_relevant_columns_details(data):
            column_description = self._build_single_column_description(column_details)
            columns_descriptions.append(column_description)

        return '/n'.join(columns_descriptions)

    def get_relevant_columns_details(self, data: DataFrame) -> Generator[ColumnDetails, None, None]:
        relevant_columns = []

        for column_name in data.columns.tolist():
            if column_name not in EXCLUDED_COLUMNS:
                relevant_columns.append(column_name)

        yield from self._generate_columns_details(data, relevant_columns)

    @staticmethod
    def _build_single_column_description(column_details: ColumnDetails) -> str:
        return SINGLE_COLUMN_DESCRIPTION_FORMAT.format(
            column_index=column_details.index + 1,
            column_name=column_details.name,
            column_operator=column_details.operator,
            column_values=column_details.values
        )


    def _generate_columns_details(self, data: DataFrame, relevant_columns: List[str]) -> Generator[ColumnDetails,
                                                                                                   None,
                                                                                                   None]:
        for column_index, column_name in enumerate(relevant_columns):
            column_dtype = data[column_name].dtype
            column_operator = self._get_column_operator(column_dtype)
            column_values = self._get_column_values(column_name, column_operator)

            yield ColumnDetails(
                index=column_index,
                name=column_name,
                operator=column_operator,
                values=column_values
            )

    @staticmethod
    def _get_column_operator(column_dtype: dtype) -> str:
        if is_string_dtype(column_dtype) or is_bool_dtype(column_dtype):
            return IN_OPERATOR

        else:
            return NUMERIC_OPERATORS

    @staticmethod
    def _get_column_values(column_name: str, column_operator: str) -> list:
        if column_operator == IN_OPERATOR:
            return get_column_possible_values(column_name)

        else:
            return get_column_min_max_values(column_name)
