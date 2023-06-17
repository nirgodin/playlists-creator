from collections import Counter
from itertools import chain
from typing import List, Tuple

import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

from server.consts.api_consts import MAX_SPOTIFY_PLAYLIST_SIZE
from server.consts.audio_features_consts import AUDIO_FEATURES, MODE, KEY, MAJOR, KEY_NAMES_MAPPING
from server.consts.data_consts import URI, GENRES, SONG, RELEASE_YEAR, RELEASE_DATE
from server.logic.playlist_imitation.playlist_details_pipeline import PlaylistDetailsPipeline
from server.logic.playlist_imitation.playlist_imitator_consts import NON_AUDIO_DATABASE_COLUMNS, DATABASE_COLUMNS, \
    SIMILARITY_SCORE, N_MOST_COMMON_GENRES, NON_NUMERIC_COLUMNS, SIMILARITY_SCORE_THRESHOLD, \
    PLAYLIST_IRRELEVANT_COLUMNS, CATEGORICAL_COLUMNS
from server.utils.data_utils import load_data
from server.utils.general_utils import sample_list
from server.utils.regex_utils import extract_year


class PlaylistImitatorTracksSelector:
    def __init__(self):
        self._key_categories = list(KEY_NAMES_MAPPING.values())

    def select_tracks(self, playlist_data: DataFrame) -> List[str]:
        filtered_database = self._filter_database(playlist_data)
        vectorized_playlist = self._average_playlist(playlist_data)
        similarity_scores = self._compute_similarity_scores(
            filtered_database.drop(NON_NUMERIC_COLUMNS, axis=1),
            vectorized_playlist
        )
        filtered_database[SIMILARITY_SCORE] = similarity_scores
        filtered_database.sort_values(by=SIMILARITY_SCORE, ascending=False, inplace=True)

        return self._select_tracks_uris(filtered_database, playlist_data[URI].tolist())

    def _filter_database(self, playlist_data: DataFrame):
        most_common_genres = self._get_most_common_genres(playlist_data)
        min_max_release_years = [int(playlist_data[RELEASE_YEAR].min()), int(playlist_data[RELEASE_YEAR].max())]
        relevant_rows = [
            i for i, row in self._database.iterrows() if self._is_relevant_row(row, most_common_genres, min_max_release_years)
        ]

        return self._database.iloc[relevant_rows]

    def _is_relevant_row(self,
                         row: Series,
                         most_common_genres: List[str],
                         min_max_release_years: List[int]) -> bool:
        if not self._has_any_relevant_genre(row, most_common_genres):
            return False

        return self._has_relevant_release_year(row, min_max_release_years)

    @staticmethod
    def _has_any_relevant_genre(row: Series, most_common_genres: List[str]) -> bool:
        row_genres = row[GENRES]
        return any(genre in most_common_genres for genre in row_genres)

    @staticmethod
    def _has_relevant_release_year(row: Series, min_max_release_years: List[int]) -> bool:
        row_release_year = row[RELEASE_YEAR]
        return min_max_release_years[0] <= row_release_year <= min_max_release_years[1]

    @staticmethod
    def _get_most_common_genres(playlist_data: DataFrame) -> List[str]:
        playlist_genres = chain.from_iterable(playlist_data[GENRES].tolist())
        genres_count = Counter(playlist_genres)
        most_common_genres = genres_count.most_common(n=N_MOST_COMMON_GENRES)

        return [genre for genre, count in most_common_genres]

    @staticmethod
    def _average_playlist(playlist_data: DataFrame) -> DataFrame:
        playlist_columns = [col for col in DATABASE_COLUMNS if col not in PLAYLIST_IRRELEVANT_COLUMNS]
        filtered_playlist_data = playlist_data[playlist_columns]

        return filtered_playlist_data.mean(axis=0)

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

    @property
    def _database(self) -> DataFrame:
        data = load_data().copy(deep=True)
        data[MODE] = data[MODE].apply(lambda x: 1 if x == MAJOR else 0)
        data[GENRES] = data[GENRES].apply(lambda x: self._serialize_track_genres(x))
        data[KEY] = pd.Categorical(data[KEY], categories=self._key_categories)
        data = pd.get_dummies(data, columns=CATEGORICAL_COLUMNS)
        data = data[[col for col in DATABASE_COLUMNS if col != KEY]]

        for column in AUDIO_FEATURES:
            if column not in NON_AUDIO_DATABASE_COLUMNS and column != KEY:
                data[column] = data[column] / 100

        return data

    @staticmethod
    def _serialize_track_genres(genres: str) -> List[str]:
        try:
            return eval(genres)
        except:
            return []


if __name__ == '__main__':
    data = pd.read_csv('/Users/nirgodin/Downloads/mock_playlist_data.csv')
    data[GENRES] = data[GENRES].apply(lambda x: eval(x))
    transformed_data = PlaylistDetailsPipeline().transform(data)
    PlaylistImitatorTracksSelector().select_tracks(transformed_data)
