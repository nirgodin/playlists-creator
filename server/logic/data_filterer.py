import random
from typing import List

import pandas as pd
from pandas import DataFrame

from server.data.query_condition import QueryCondition


class DataFilterer:
    def __init__(self, candidates_pool_size: int = 5000, max_playlist_size: int = 100):
        self._candidates_pool_size = candidates_pool_size
        self._max_playlist_size = max_playlist_size
        self._data = pd.read_csv(r'groubyed_songs.csv')

    def filter(self, query_conditions: List[QueryCondition]) -> DataFrame:
        query = self._build_query(query_conditions)
        filtered_data = self._data.query(query).reset_index(drop=True)
        candidates_data = self._generate_candidates(filtered_data)

        return candidates_data.iloc[:self._max_playlist_size]

    def _generate_candidates(self, filtered_data: DataFrame) -> DataFrame:
        if filtered_data.empty:
            return filtered_data

        max_candidates = len(filtered_data)
        candidates_indexes = [random.randint(0, max_candidates) for i in range(max_candidates)]
        candidates = self._data.iloc[candidates_indexes]
        candidates.reset_index(drop=True, inplace=True)

        return candidates

    @staticmethod
    def _build_query(query_conditions: List[QueryCondition]) -> str:
        conditions = [query_condition.condition for query_condition in query_conditions]
        return ' and '.join(conditions)


if __name__ == '__main__':
    query_conditions = [
        QueryCondition(
            column='duration_ms',
            operator='<',
            value=240000
        ),
        QueryCondition(
            column='energy',
            operator='<',
            value=0.8
        ),
        QueryCondition(
            column='energy',
            operator='<',
            value=0.8
        ),
        QueryCondition(
            column='energy',
            operator='>',
            value=0.4
        ),
        QueryCondition(
            column='explicit',
            operator='==',
            value=True
        ),
        QueryCondition(
            column='tempo',
            operator='>',
            value=100
        ),
        QueryCondition(
            column='median_popularity',
            operator='<',
            value=80
        ),
        QueryCondition(
            column='median_popularity',
            operator='>',
            value=40
        )
    ]
    DataFilterer().filter(query_conditions)
