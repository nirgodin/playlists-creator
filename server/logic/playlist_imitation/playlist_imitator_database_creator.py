import pandas as pd
from pandas import DataFrame

from server.consts.audio_features_consts import NUMERIC_AUDIO_FEATURES, NON_MULTIPLIED_AUDIO_FEATURES
from server.consts.path_consts import PLAYLIST_IMITATOR_DATABASE_PATH
from server.logic.playlist_imitation.playlist_details_pipeline import PlaylistDetailsPipeline


class PlaylistImitatorDatabaseCreator:
    def __init__(self):
        self._playlist_details_pipeline = PlaylistDetailsPipeline(is_training=True)

    def create_database(self, raw_data: DataFrame) -> None:
        data = raw_data.copy(deep=True)
        normalized_audio_features_data = self._normalize_audio_features(data)
        transformed_data = self._playlist_details_pipeline.transform(normalized_audio_features_data)
        print('b')

        # transformed_data.to_csv(PLAYLIST_IMITATOR_DATABASE_PATH, index=False)

    @staticmethod
    def _normalize_audio_features(data: DataFrame) -> DataFrame:
        for column in NUMERIC_AUDIO_FEATURES:
            if column not in NON_MULTIPLIED_AUDIO_FEATURES:
                data[column] = data[column] / 100

        return data


if __name__ == '__main__':
    data = pd.read_csv('/Users/nirgodin/dev/playlists-creator/server/resources/playlists_creator_database.csv')
    PlaylistImitatorDatabaseCreator().create_database(data)
