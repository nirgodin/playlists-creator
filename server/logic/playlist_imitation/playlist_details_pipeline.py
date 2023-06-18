import os.path
import pickle

import pandas as pd
from pandas import DataFrame
from pandas.core.dtypes.common import is_string_dtype, is_numeric_dtype
from sklearn.base import BaseEstimator
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

from server.consts.audio_features_consts import KEY_NAMES_MAPPING, KEY, MODE, MAJOR
from server.consts.data_consts import RELEASE_YEAR, RELEASE_DATE
from server.consts.path_consts import PLAYLIST_IMITATOR_PIPELINE_RESOURCES_DIR, \
    PLAYLIST_IMITATOR_SCALER_FILENAME, PLAYLIST_IMITATOR_IMPUTER_FILENAME
from server.logic.playlist_imitation.playlist_imitator_consts import CATEGORICAL_COLUMNS, DATABASE_COLUMNS
from server.logic.playlist_imitation.playlist_imitator_resources import PlaylistImitatorResources
from server.utils.data_utils import sort_data_columns_alphabetically
from server.utils.regex_utils import extract_year


class PlaylistDetailsPipeline:
    def __init__(self, is_training: bool):
        self._is_training = is_training
        self._key_categories = list(KEY_NAMES_MAPPING.values())

    def transform(self, raw_data: DataFrame) -> DataFrame:
        if is_string_dtype(raw_data[MODE]):
            raw_data[MODE] = raw_data[MODE].apply(lambda x: 1 if x == MAJOR else 0)

        if RELEASE_YEAR not in raw_data.columns:
            raw_data[RELEASE_YEAR] = raw_data[RELEASE_DATE].apply(lambda x: extract_year(x))

        one_hot_data = self._encode_dummy_columns(raw_data)
        data_subset = one_hot_data[DATABASE_COLUMNS]
        sorted_data = sort_data_columns_alphabetically(data_subset)

        return self._apply_transformations(sorted_data)

    def _encode_dummy_columns(self, data: DataFrame) -> DataFrame:
        if is_numeric_dtype(data[KEY]):
            data[KEY] = data[KEY].map(KEY_NAMES_MAPPING)

        data[KEY] = pd.Categorical(data[KEY], categories=self._key_categories)
        return pd.get_dummies(data, columns=CATEGORICAL_COLUMNS)

    def _apply_transformations(self, data: DataFrame) -> DataFrame:
        numeric_columns = [col for col in data.columns if is_numeric_dtype(data[col])]
        pipeline_resources = self._load_pipeline_resources()
        columns_transformer = ColumnTransformer(
            verbose_feature_names_out=False,
            remainder='passthrough',
            transformers=[
                (
                    'pipeline',
                    Pipeline(
                        [
                            ('imputer', pipeline_resources.imputer),
                            ('scaler', pipeline_resources.scaler)
                        ]
                    ),
                    numeric_columns
                )
            ]
        )
        columns_transformer.set_output(transform='pandas')
        transformed_data = getattr(columns_transformer, pipeline_resources.method)(data)
        self._dump_pipeline_resources(pipeline_resources)

        return transformed_data

    def _load_pipeline_resources(self) -> PlaylistImitatorResources:
        if self._is_training:
            return PlaylistImitatorResources(
                imputer=SimpleImputer(),
                scaler=MinMaxScaler(),
                method='fit_transform'
            )

        return PlaylistImitatorResources(
            imputer=self._load_single_pipeline_resource(PLAYLIST_IMITATOR_IMPUTER_FILENAME),
            scaler=self._load_single_pipeline_resource(PLAYLIST_IMITATOR_SCALER_FILENAME),
            method='transform'
        )

    def _dump_pipeline_resources(self, pipeline_resources: PlaylistImitatorResources) -> None:
        if pipeline_resources.method == 'transform':
            return

        self._dump_single_pipeline_resource(pipeline_resources.imputer, PLAYLIST_IMITATOR_IMPUTER_FILENAME)
        self._dump_single_pipeline_resource(pipeline_resources.scaler, PLAYLIST_IMITATOR_SCALER_FILENAME)

    @staticmethod
    def _load_single_pipeline_resource(file_name: str) -> BaseEstimator:
        path = os.path.join(PLAYLIST_IMITATOR_PIPELINE_RESOURCES_DIR, file_name)

        with open(path, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def _dump_single_pipeline_resource(estimator: BaseEstimator, file_name: str) -> None:
        path = os.path.join(PLAYLIST_IMITATOR_PIPELINE_RESOURCES_DIR, file_name)

        with open(path, 'wb') as f:
            pickle.dump(estimator, f)
