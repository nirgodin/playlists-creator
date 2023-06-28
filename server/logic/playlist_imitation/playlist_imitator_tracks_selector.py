from collections import Counter
from collections import Counter
from itertools import chain
from typing import List, Tuple

import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from tqdm import tqdm

from server.consts.api_consts import MAX_SPOTIFY_PLAYLIST_SIZE
from server.consts.data_consts import URI, GENRES, RELEASE_YEAR, POPULARITY, ARTIST_POPULARITY
from server.consts.path_consts import PLAYLIST_IMITATOR_DATABASE_PATH
from server.logic.playlist_imitation.playlist_imitator_consts import DATABASE_COLUMNS, \
    SIMILARITY_SCORE, N_MOST_COMMON_GENRES, NON_NUMERIC_COLUMNS, SIMILARITY_SCORE_THRESHOLD, \
    PLAYLIST_IRRELEVANT_COLUMNS, KEY_COLUMNS
from server.utils.general_utils import sample_list

NUMERIC_RANGE_FILTER_COLUMNS = [
    RELEASE_YEAR,
    POPULARITY,
    ARTIST_POPULARITY
]


class PlaylistImitatorTracksSelector:
    def __init__(self):
        self._database = pd.read_csv(
            filepath_or_buffer=PLAYLIST_IMITATOR_DATABASE_PATH,
            converters={
                GENRES: lambda x: self._serialize_track_genres(x)
            }
        )

    def select_tracks(self, playlist_data: DataFrame) -> List[str]:
        filtered_database = self._filter_database(playlist_data)
        vectorized_playlist = self._average_playlist(playlist_data)
        similarity_scores = self._compute_similarity_scores(
            filtered_database.drop(NON_NUMERIC_COLUMNS + NUMERIC_RANGE_FILTER_COLUMNS + KEY_COLUMNS, axis=1),
            vectorized_playlist.drop(NUMERIC_RANGE_FILTER_COLUMNS + KEY_COLUMNS, axis=1)
        )
        filtered_database[SIMILARITY_SCORE] = similarity_scores
        filtered_database.sort_values(by=SIMILARITY_SCORE, ascending=False, inplace=True)

        return self._select_tracks_uris(filtered_database, playlist_data[URI].tolist())

    def _filter_database(self, playlist_data: DataFrame):
        most_common_genres = self._get_most_common_genres(playlist_data)
        pipeline = Pipeline(
            [
                ('genres', FunctionTransformer(lambda x: self._filter_non_relevant_genres(x, most_common_genres))),
                ('range_values', FunctionTransformer(lambda x: self._filter_out_of_range_values(x, NUMERIC_RANGE_FILTER_COLUMNS))),
            ]
        )

        return pipeline.transform(self._database)

    @staticmethod
    def _get_most_common_genres(playlist_data: DataFrame) -> List[str]:
        playlist_genres = chain.from_iterable(playlist_data[GENRES].tolist())
        genres_count = Counter(playlist_genres)
        most_common_genres = genres_count.most_common(n=N_MOST_COMMON_GENRES)

        return [genre for genre, count in most_common_genres]

    @staticmethod
    def _get_series_interquartile_percentiles_values(series: Series) -> Tuple[float, float]:
        return float(series.quantile(0.25)), float(series.quantile(0.75))

    @staticmethod
    def _has_any_relevant_genre(genres: List[str], most_common_genres: List[str]) -> bool:
        return any(genre in most_common_genres for genre in genres)

    def _filter_out_of_range_values(self, data: DataFrame, columns: List[str]) -> DataFrame:
        for column in columns:
            interquartile_range = self._get_series_interquartile_percentiles_values(data[column])
            query = f"`{column}` >= {interquartile_range[0]} and `{column}` <= {interquartile_range[1]}"
            data = data.query(query)

        return data

    def _filter_non_relevant_genres(self, data: DataFrame, most_common_genres: List[str]) -> bool:
        data['has_any_relevant_genre'] = data['genres'].apply(lambda x: self._has_any_relevant_genre(x, most_common_genres))
        data = data[data['has_any_relevant_genre'] == True]
        data.drop('has_any_relevant_genre', axis=1, inplace=True)

        return data

    @staticmethod
    def _average_playlist(playlist_data: DataFrame) -> DataFrame:
        playlist_columns = [col for col in DATABASE_COLUMNS if col not in PLAYLIST_IRRELEVANT_COLUMNS]
        filtered_playlist_data = playlist_data[playlist_columns]

        return filtered_playlist_data.mean(axis=0).to_frame().transpose()

    @staticmethod
    def _compute_similarity_scores(filtered_database: DataFrame, averaged_playlist: DataFrame) -> List[float]:
        scores = []
        vectorized_playlist = np.array(averaged_playlist).reshape(1, -1)

        with tqdm(total=len(filtered_database)) as progress_bar:
            for i in range(len(filtered_database)):
                try:
                    database_vector = np.array(filtered_database.iloc[i]).reshape(1, -1)
                    similarity = cosine_similarity(vectorized_playlist, database_vector)[0][0]
                except:
                    similarity = np.nan

                scores.append(similarity)
                progress_bar.update(1)

        return scores

    def _select_tracks_uris(self, filtered_database: DataFrame, existing_uris: List[str]) -> List[str]:
        uris = self._filter_relevant_uris(filtered_database, existing_uris)
        n_candidates = len(uris)
        n_selected_candidates = min(n_candidates, MAX_SPOTIFY_PLAYLIST_SIZE)
        uris_indexes = sample_list(n_candidates, n_selected_candidates)

        return [uris[i] for i in uris_indexes]

    @staticmethod
    def _filter_relevant_uris(filtered_database: DataFrame, existing_uris: List[str]) -> List[str]:
        relevant_uris = []

        for uri, similarity_score in zip(filtered_database[URI], filtered_database[SIMILARITY_SCORE]):
            if uri not in existing_uris and similarity_score > SIMILARITY_SCORE_THRESHOLD:
                relevant_uris.append(uri)

        return relevant_uris

    @staticmethod
    def _serialize_track_genres(genres: str) -> List[str]:
        try:
            return eval(genres)
        except SyntaxError:
            return []


if __name__ == '__main__':
    data = pd.read_csv('/Users/nirgodin/Downloads/mock_morning_playlist_data.csv')
    # data['song'] = ''
    data[GENRES] = data[GENRES].apply(lambda x: eval(x))
    # transformed_data = PlaylistDetailsPipeline(is_training=False).transform(data)
    PlaylistImitatorTracksSelector().select_tracks(data)
