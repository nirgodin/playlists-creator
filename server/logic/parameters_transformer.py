import re
from typing import List

from server.consts.app_consts import FILTER_PARAMS
from server.data.query_condition import QueryCondition


class ParametersTransformer:
    def transform(self, body: dict) -> List[QueryCondition]:
        filter_params = body[FILTER_PARAMS]
        return self._pre_process_request_body(filter_params)

    def _pre_process_request_body(self, filter_params: dict) -> List[QueryCondition]:
        pre_processed_body = []

        for column_name, column_details in filter_params.items():
            query_condition = self._pre_process_single_column_details(column_name, column_details)

            if query_condition.condition is not None:
                pre_processed_body.append(query_condition)

        return pre_processed_body

    def _pre_process_single_column_details(self, column_name: str, column_details: dict) -> QueryCondition:
        pre_processed_column_name = self._pre_process_column_name(column_name)
        pre_processed_details = {'column': pre_processed_column_name}
        pre_processed_details.update(column_details)
        return QueryCondition.from_dict(pre_processed_details)

    def _pre_process_column_name(self, column_name: str) -> str:
        snakecased_column_name = self._to_snakecase(column_name)
        return re.sub(r'min_|max_', '', snakecased_column_name)

    @staticmethod
    def _to_snakecase(s: str) -> str:
        result = ""

        for i, char in enumerate(s):
            if char.isupper() and i != 0:
                result += "_"
            result += char.lower()

        return result
