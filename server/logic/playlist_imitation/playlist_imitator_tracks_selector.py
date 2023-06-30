from typing import List

import numpy as np
import pandas as pd
from numpy import ndarray
from pandas import DataFrame, Series
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

from server.consts.api_consts import MAX_SPOTIFY_PLAYLIST_SIZE
from server.consts.data_consts import URI, GENRES
from server.logic.playlist_imitation.playlist_imitator_consts import DATABASE_COLUMNS, \
    SIMILARITY_SCORE, NON_NUMERIC_COLUMNS, SIMILARITY_SCORE_THRESHOLD, \
    PLAYLIST_IRRELEVANT_COLUMNS, NUMERIC_RANGE_FILTER_COLUMNS
from server.logic.playlist_imitation.playlist_imitator_database_filterer import PlaylistImitatorDatabaseFilterer
from server.utils.general_utils import sample_list


class PlaylistImitatorTracksSelector:
    def __init__(self):
        self._database_filterer = PlaylistImitatorDatabaseFilterer()

    def select_tracks(self, playlist_data: DataFrame) -> List[str]:
        filtered_database = self._database_filterer.filter(playlist_data)
        vectorized_playlist = self._average_playlist(playlist_data)
        similarity_scores = self._compute_similarity_scores(
            filtered_database.drop(NON_NUMERIC_COLUMNS + NUMERIC_RANGE_FILTER_COLUMNS, axis=1),
            vectorized_playlist.drop(NUMERIC_RANGE_FILTER_COLUMNS, axis=1)
        )
        filtered_database[SIMILARITY_SCORE] = similarity_scores
        filtered_database.sort_values(by=SIMILARITY_SCORE, ascending=False, inplace=True)

        return self._select_tracks_uris(filtered_database, playlist_data[URI].tolist())

    @staticmethod
    def _average_playlist(playlist_data: DataFrame) -> DataFrame:
        playlist_columns = [col for col in DATABASE_COLUMNS if col not in PLAYLIST_IRRELEVANT_COLUMNS]
        filtered_playlist_data = playlist_data[playlist_columns]

        return filtered_playlist_data.median(axis=0).to_frame().transpose()

    def _compute_similarity_scores(self, filtered_database: DataFrame, averaged_playlist: DataFrame) -> List[float]:
        scores = []
        vectorized_playlist = self._vectorize(averaged_playlist).reshape(1, -1)
        vectorized_database = self._vectorize(filtered_database)
        n_records = len(filtered_database)

        with tqdm(total=n_records) as progress_bar:
            for i in range(n_records):
                similarity = self._compute_single_similarity_score(vectorized_playlist, vectorized_database[i])
                scores.append(similarity)
                progress_bar.update(1)

        return scores

    @staticmethod
    def _vectorize(data: DataFrame) -> ndarray:
        sorted_columns_data = data[sorted(data.columns)]
        return sorted_columns_data.to_numpy()

    @staticmethod
    def _compute_single_similarity_score(vectorized_playlist: ndarray, database_row: ndarray) -> float:
        try:
            vectorized_database_row = database_row.reshape(1, -1)
            return cosine_similarity(vectorized_playlist, vectorized_database_row)[0][0]

        except:
            return np.nan

    def _select_tracks_uris(self, filtered_database: DataFrame, existing_uris: List[str]) -> List[str]:
        uris = self._filter_relevant_uris(filtered_database, existing_uris)
        n_candidates = len(uris)
        uris_indexes = sample_list(n_candidates, MAX_SPOTIFY_PLAYLIST_SIZE)

        return [uris[i] for i in uris_indexes]

    @staticmethod
    def _filter_relevant_uris(filtered_database: DataFrame, existing_uris: List[str]) -> List[str]:
        relevant_uris = []

        for uri, similarity_score in zip(filtered_database[URI], filtered_database[SIMILARITY_SCORE]):
            if uri not in existing_uris and similarity_score > SIMILARITY_SCORE_THRESHOLD:
                relevant_uris.append(uri)

        return relevant_uris


if __name__ == '__main__':
    data = pd.read_csv('/Users/nirgodin/Downloads/mock_morning_playlist_data.csv')
    # data['song'] = ''
    data[GENRES] = data[GENRES].apply(lambda x: eval(x))
    # transformed_data = PlaylistDetailsPipeline(is_training=False).transform(data)
    PlaylistImitatorTracksSelector().select_tracks(data)
