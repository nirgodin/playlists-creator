from typing import List

from pandas import DataFrame

from server.consts.data_consts import URI
from server.logic.playlist_imitation.playlist_imitator_consts import DATABASE_COLUMNS, \
    SIMILARITY_SCORE, NON_NUMERIC_COLUMNS, SIMILARITY_SCORE_THRESHOLD, \
    PLAYLIST_IRRELEVANT_COLUMNS, NUMERIC_RANGE_FILTER_COLUMNS
from server.logic.playlist_imitation.playlist_imitator_database_filterer import PlaylistImitatorDatabaseFilterer
from server.logic.similarity_scores_computer import SimilarityScoresComputer
from server.utils.spotify_utils import sample_uris


class PlaylistImitatorTracksSelector:
    def __init__(self):
        self._database_filterer = PlaylistImitatorDatabaseFilterer()
        self._similarity_scores_computer = SimilarityScoresComputer()

    def select_tracks(self, playlist_data: DataFrame) -> List[str]:
        filtered_database = self._database_filterer.filter(playlist_data)
        vectorized_playlist = self._average_playlist(playlist_data)
        similarity_scores = self._similarity_scores_computer.compute_similarity_scores(
            database=filtered_database.drop(NON_NUMERIC_COLUMNS + NUMERIC_RANGE_FILTER_COLUMNS, axis=1),
            candidate=vectorized_playlist.drop(NUMERIC_RANGE_FILTER_COLUMNS, axis=1)
        )
        filtered_database[SIMILARITY_SCORE] = similarity_scores
        filtered_database.sort_values(by=SIMILARITY_SCORE, ascending=False, inplace=True)

        return self._select_tracks_uris(filtered_database, playlist_data[URI].tolist())

    @staticmethod
    def _average_playlist(playlist_data: DataFrame) -> DataFrame:
        playlist_columns = [col for col in DATABASE_COLUMNS if col not in PLAYLIST_IRRELEVANT_COLUMNS]
        filtered_playlist_data = playlist_data[playlist_columns]

        return filtered_playlist_data.median(axis=0).to_frame().transpose()

    def _select_tracks_uris(self, filtered_database: DataFrame, existing_uris: List[str]) -> List[str]:
        uris = self._filter_relevant_uris(filtered_database, existing_uris)
        return sample_uris(uris)

    @staticmethod
    def _filter_relevant_uris(filtered_database: DataFrame, existing_uris: List[str]) -> List[str]:
        relevant_uris = []

        for uri, similarity_score in zip(filtered_database[URI], filtered_database[SIMILARITY_SCORE]):
            if uri not in existing_uris and similarity_score > SIMILARITY_SCORE_THRESHOLD:
                relevant_uris.append(uri)

        return relevant_uris
