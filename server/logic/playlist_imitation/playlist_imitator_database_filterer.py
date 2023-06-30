from collections import Counter
from itertools import chain
from typing import List, Tuple

import pandas as pd
from pandas import DataFrame, Series
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer

from server.consts.data_consts import GENRES
from server.consts.path_consts import PLAYLIST_IMITATOR_DATABASE_PATH
from server.logic.playlist_imitation.playlist_imitator_consts import N_MOST_COMMON_GENRES, NUMERIC_RANGE_FILTER_COLUMNS, \
    HAS_RELEVANT_GENRES, SERIES, Z_SCORE, OUTLIER_THRESHOLD
from server.utils.statistics_utils import calculate_z_score


class PlaylistImitatorDatabaseFilterer:
    def __init__(self):
        self._database = pd.read_csv(
            filepath_or_buffer=PLAYLIST_IMITATOR_DATABASE_PATH,
            converters={
                GENRES: lambda x: self._serialize_track_genres(x)
            }
        )

    def filter(self, playlist_data: DataFrame) -> DataFrame:
        most_common_genres = self._get_most_common_genres(playlist_data)
        pipeline = make_pipeline(
            FunctionTransformer(
                lambda x: self._filter_non_relevant_genres(x, most_common_genres)
            ),
            FunctionTransformer(
                lambda x: self._filter_out_of_range_values(x, playlist_data, NUMERIC_RANGE_FILTER_COLUMNS)
            )
        )
        database = self._database.copy(deep=True)

        return pipeline.transform(database)

    @staticmethod
    def _get_most_common_genres(playlist_data: DataFrame) -> List[str]:
        playlist_genres = chain.from_iterable(playlist_data[GENRES].tolist())
        genres_count = Counter(playlist_genres)
        most_common_genres = genres_count.most_common(n=N_MOST_COMMON_GENRES)

        return [genre for genre, count in most_common_genres]

    def _filter_non_relevant_genres(self, data: DataFrame, most_common_genres: List[str]) -> bool:
        data[HAS_RELEVANT_GENRES] = data[GENRES].apply(lambda x: self._has_any_relevant_genre(x, most_common_genres))
        data = data[data[HAS_RELEVANT_GENRES] == True]

        return data.drop(HAS_RELEVANT_GENRES, axis=1)

    @staticmethod
    def _has_any_relevant_genre(genres: List[str], most_common_genres: List[str]) -> bool:
        return any(genre in most_common_genres for genre in genres)

    def _filter_out_of_range_values(self, data: DataFrame, playlist_data: DataFrame, columns: List[str]) -> DataFrame:
        for column in columns:
            min_value, max_value = self._get_series_non_outlier_min_max_values(playlist_data[column])
            query = f"`{column}` >= {min_value} and `{column}` <= {max_value}"
            data = data.query(query)

        return data

    @staticmethod
    def _get_series_non_outlier_min_max_values(series: Series) -> Tuple[float, float]:
        data = series.to_frame(SERIES)
        mean = data[SERIES].mean()
        std = data[SERIES].std()
        data[Z_SCORE] = data[SERIES].apply(lambda x: abs(calculate_z_score(x, mean, std)))
        non_outlier_data = data[data[Z_SCORE] < OUTLIER_THRESHOLD][SERIES]

        return float(non_outlier_data.min()), float(non_outlier_data.max())

    @staticmethod
    def _serialize_track_genres(genres: str) -> List[str]:
        try:
            return eval(genres)
        except SyntaxError:
            return []
