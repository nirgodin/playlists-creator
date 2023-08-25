from typing import List

import pandas as pd

from server.consts.data_consts import URI
from server.consts.path_consts import DATA_PATH
from server.data.query_condition import QueryCondition


class DataFilterer:
    def __init__(self):
        self._data = pd.read_csv(DATA_PATH)

    def filter(self, query_conditions: List[QueryCondition]) -> List[str]:
        query = self._build_query(query_conditions)
        filtered_data = self._data.query(query).reset_index(drop=True)

        return filtered_data[URI].tolist()

    @staticmethod
    def _build_query(query_conditions: List[QueryCondition]) -> str:
        conditions = [query_condition.condition for query_condition in query_conditions]
        return ' and '.join(conditions)
