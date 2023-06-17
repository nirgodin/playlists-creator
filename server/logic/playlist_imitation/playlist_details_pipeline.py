import pandas as pd
from pandas import DataFrame

from server.consts.audio_features_consts import KEY_NAMES_MAPPING, KEY
from server.consts.data_consts import RELEASE_YEAR, RELEASE_DATE
from server.logic.playlist_imitation.playlist_imitator_consts import CATEGORICAL_COLUMNS
from server.utils.regex_utils import extract_year


class PlaylistDetailsPipeline:
    def __init__(self):
        self._key_categories = list(KEY_NAMES_MAPPING.values())

    def transform(self, data: DataFrame) -> DataFrame:
        data[RELEASE_YEAR] = data[RELEASE_DATE].apply(lambda x: extract_year(x))
        one_hot_data = self._encode_dummy_columns(data)

        return one_hot_data

    def _encode_dummy_columns(self, data: DataFrame) -> DataFrame:
        data[KEY] = data[KEY].map(KEY_NAMES_MAPPING)
        data[KEY] = pd.Categorical(data[KEY], categories=self._key_categories)

        return pd.get_dummies(data, columns=CATEGORICAL_COLUMNS)
