import random
from typing import List

import pandas as pd
from pandas import DataFrame

from server.consts.data_consts import DATA_PATH, URI
from server.data.query_condition import QueryCondition
from server.utils import sample_list


class DataFilterer:
    def __init__(self, candidates_pool_size: int = 5000, max_playlist_size: int = 100):
        self._candidates_pool_size = candidates_pool_size
        self._max_playlist_size = max_playlist_size
        self._data = pd.read_csv(DATA_PATH)

    def filter(self, query_conditions: List[QueryCondition]) -> List[str]:
        query = self._build_query(query_conditions)
        filtered_data = self._data.query(query).reset_index(drop=True)
        candidates_data = self._generate_candidates(filtered_data)

        return candidates_data[URI].tolist()

    def _generate_candidates(self, filtered_data: DataFrame) -> DataFrame:
        if filtered_data.empty:
            return filtered_data

        n_candidates = len(filtered_data)
        n_selected_candidates = min(self._max_playlist_size, n_candidates)
        candidates_indexes = sample_list(n_candidates, n_selected_candidates)

        return self._data.iloc[candidates_indexes]

    @staticmethod
    def _build_query(query_conditions: List[QueryCondition]) -> str:
        conditions = [query_condition.condition for query_condition in query_conditions]
        return ' and '.join(conditions)
