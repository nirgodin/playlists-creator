from typing import List

import pandas as pd
from _pytest.fixtures import fixture
from pandas import DataFrame
from pandas._testing import assert_frame_equal

from server.data.track_features import TrackFeatures
from server.logic.playlist_imitation.playlist_details_serializer import PlaylistDetailsSerializer
from server.utils.data_utils import sort_data_columns_alphabetically
from server.utils.regex_utils import extract_year


class TestPlaylistDetailsSerializer:
    def test_serialize(self, serializer: PlaylistDetailsSerializer, tracks_features: List[TrackFeatures], expected: DataFrame):
        actual = serializer.serialize(tracks_features)
        assert_frame_equal(actual, expected)

    @fixture(scope="class")
    def serializer(self) -> PlaylistDetailsSerializer:
        return PlaylistDetailsSerializer()

    @fixture(scope="class")
    def expected(self, tracks_features: List[TrackFeatures]) -> DataFrame:
        records = [self._to_record(track) for track in tracks_features]
        data = pd.DataFrame.from_records(records)

        return sort_data_columns_alphabetically(data)

    @staticmethod
    def _to_record(track_features: TrackFeatures) -> dict:
        return {
            'acousticness': track_features.audio['acousticness'],
            'danceability': track_features.audio['danceability'],
            'duration_ms': track_features.audio['duration_ms'],
            'energy': track_features.audio['energy'],
            'instrumentalness': track_features.audio['instrumentalness'],
            'key': track_features.audio['key'],
            'liveness': track_features.audio['liveness'],
            'loudness': track_features.audio['loudness'],
            'mode': track_features.audio['mode'],
            'speechiness': track_features.audio['speechiness'],
            'tempo': track_features.audio['tempo'],
            'time_signature': track_features.audio['time_signature'],
            'valence': track_features.audio['valence'],
            'release_year': extract_year(track_features.track['album']['release_date']),
            'explicit': track_features.track['explicit'],
            'popularity': track_features.track['popularity'],
            'track_number': track_features.track['track_number'],
            'artist_followers': track_features.artist['followers']['total'],
            'artist_popularity': track_features.artist['popularity']
        }
