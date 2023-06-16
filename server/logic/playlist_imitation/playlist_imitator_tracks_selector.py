from collections import Counter
from itertools import chain
from typing import List

import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

from server.consts.api_consts import MAX_SPOTIFY_PLAYLIST_SIZE
from server.consts.audio_features_consts import AUDIO_FEATURES, MODE, KEY, MAJOR
from server.consts.data_consts import URI, MAIN_GENRE, SONG, GENRES
from server.utils.data_utils import load_data
from server.utils.general_utils import sample_list

ARTIST_GENRES = 'artist_genres'
NON_AUDIO_DATABASE_COLUMNS = [
    URI,
    GENRES,
    SONG
]
DATABASE_COLUMNS = AUDIO_FEATURES + NON_AUDIO_DATABASE_COLUMNS
CATEGORICAL_FILTER_COLUMNS = [
    MAIN_GENRE
]
SIMILARITY_SCORE = 'similarity_score'
N_MOST_COMMON_GENRES = 3
KEY_NAMES_MAPPING = {
    0: 'C',
    1: 'C#',
    2: 'D',
    3: 'D#',
    4: 'E',
    5: 'F',
    6: 'F#',
    7: 'G',
    8: 'G#',
    9: 'A',
    10: 'A#',
    11: 'B'
}


class PlaylistImitatorTracksSelector:
    def __init__(self):
        self._key_categories = list(KEY_NAMES_MAPPING.values())

    def select_tracks(self, playlist_data: DataFrame) -> List[str]:
        filtered_database = self._filter_database(playlist_data)
        vectorized_playlist = self._average_playlist(playlist_data)
        similarity_scores = self._compute_similarity_scores(
            filtered_database.drop(NON_AUDIO_DATABASE_COLUMNS, axis=1),
            vectorized_playlist
        )
        filtered_database[SIMILARITY_SCORE] = similarity_scores
        filtered_database.sort_values(by=SIMILARITY_SCORE, ascending=False, inplace=True)

        return self._select_tracks_uris(filtered_database, playlist_data['uri'].tolist())

    def _filter_database(self, playlist_data: DataFrame):
        most_common_genres = self._get_most_common_genres(playlist_data)
        relevant_rows = [i for i, row in self._database.iterrows() if self._has_any_relevant_genre(row, most_common_genres)]

        return self._database.iloc[relevant_rows]

    @staticmethod
    def _has_any_relevant_genre(row: Series, most_common_genres) -> bool:
        row_genres = row[GENRES]
        return any(genre in most_common_genres for genre in row_genres)

    @staticmethod
    def _get_most_common_genres(playlist_data: DataFrame) -> List[str]:
        playlist_genres = chain.from_iterable(playlist_data[ARTIST_GENRES].tolist())
        genres_count = Counter(playlist_genres)
        most_common_genres = genres_count.most_common(n=N_MOST_COMMON_GENRES)

        return [genre for genre, count in most_common_genres]

    def _average_playlist(self, playlist_data: DataFrame) -> DataFrame:
        playlist_data.columns = [col.replace('track_', '') for col in playlist_data.columns]
        filtered_playlist_data = playlist_data[[col for col in DATABASE_COLUMNS if col not in ['song', GENRES]]]
        filtered_playlist_data[KEY] = filtered_playlist_data[KEY].map(KEY_NAMES_MAPPING)
        filtered_playlist_data[KEY] = pd.Categorical(filtered_playlist_data[KEY], categories=self._key_categories)
        one_hot_data = pd.get_dummies(filtered_playlist_data, columns=[KEY])

        return one_hot_data.mean(axis=0)

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

    @staticmethod
    def _select_tracks_uris(filtered_database: DataFrame, existing_uris: List[str]) -> List[str]:
        uris = [uri for uri in filtered_database[URI].tolist() if uri not in existing_uris]
        uris_indexes = sample_list(len(uris), MAX_SPOTIFY_PLAYLIST_SIZE)

        return [uris[i] for i in uris_indexes]

    @property
    def _database(self) -> DataFrame:
        raw_database = load_data()
        data = raw_database[DATABASE_COLUMNS]
        data[MODE] = data[MODE].apply(lambda x: 1 if x == MAJOR else 0)
        data[GENRES] = data[GENRES].apply(lambda x: self._serialize_track_genres(x))
        data[KEY] = pd.Categorical(data[KEY], categories=self._key_categories)

        for column in AUDIO_FEATURES:
            if column not in NON_AUDIO_DATABASE_COLUMNS and column != KEY:
                data[column] = data[column] / 100

        return pd.get_dummies(data, columns=[KEY])

    @staticmethod
    def _serialize_track_genres(genres: str) -> List[str]:
        try:
            return eval(genres)
        except:
            return []


if __name__ == '__main__':
    data = pd.read_csv('/Users/nirgodin/Downloads/invalid_playlist_data.csv')
    data[ARTIST_GENRES] = data[ARTIST_GENRES].apply(lambda x: eval(x))
    PlaylistImitatorTracksSelector().select_tracks(data)
