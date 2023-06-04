from typing import List

from server.consts.app_consts import FILTER_PARAMS
from server.data.query_condition import QueryCondition
from server.utils.string_utils import pre_process_column_name


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

    @staticmethod
    def _pre_process_single_column_details(column_name: str, column_details: dict) -> QueryCondition:
        pre_processed_column_name = pre_process_column_name(column_name)
        pre_processed_details = {'column': pre_processed_column_name}
        pre_processed_details.update(column_details)

        return QueryCondition.from_dict(pre_processed_details)
