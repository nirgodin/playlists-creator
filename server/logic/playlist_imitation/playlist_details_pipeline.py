import os.path
import pickle
from typing import List

from pandas import DataFrame
from pandas.core.dtypes.common import is_string_dtype, is_numeric_dtype
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

from server.consts.audio_features_consts import KEY_NAMES_MAPPING, MODE, MAJOR
from server.consts.data_consts import RELEASE_YEAR, RELEASE_DATE
from server.consts.path_consts import PLAYLIST_IMITATOR_PIPELINE_RESOURCES_DIR, PLAYLIST_IMITATOR_PIPELINE
from server.logic.playlist_imitation.playlist_imitator_consts import DATABASE_COLUMNS
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

        data_subset = raw_data[DATABASE_COLUMNS]
        sorted_data = sort_data_columns_alphabetically(data_subset)

        return self._apply_transformations(sorted_data)

    def _apply_transformations(self, data: DataFrame) -> DataFrame:
        numeric_columns = [col for col in data.columns if is_numeric_dtype(data[col])]
        pipeline_resources = self._load_pipeline_resources(numeric_columns)
        transformed_data = getattr(pipeline_resources.pipeline, pipeline_resources.method)(data)
        self._dump_pipeline(pipeline_resources)

        return transformed_data

    def _load_pipeline_resources(self, numeric_columns: List[str]) -> PlaylistImitatorResources:
        if self._is_training:
            return PlaylistImitatorResources(
                pipeline=self._create_new_pipeline(numeric_columns),
                method='fit_transform'
            )

        return PlaylistImitatorResources(
            pipeline=self._load_pipeline(),
            method='transform'
        )

    @staticmethod
    def _create_new_pipeline(numeric_columns: List[str]) -> ColumnTransformer:
        column_transformer = ColumnTransformer(
            verbose_feature_names_out=False,
            remainder='passthrough',
            transformers=[
                (
                    'pipeline',
                    Pipeline(
                        [
                            ('imputer', SimpleImputer(strategy='median')),
                            ('scaler', MinMaxScaler())
                        ]
                    ),
                    numeric_columns
                )
            ]
        )
        column_transformer.set_output(transform='pandas')

        return column_transformer

    @staticmethod
    def _load_pipeline() -> ColumnTransformer:
        path = os.path.join(PLAYLIST_IMITATOR_PIPELINE_RESOURCES_DIR, PLAYLIST_IMITATOR_PIPELINE)

        with open(path, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def _dump_pipeline(pipeline_resources: PlaylistImitatorResources) -> None:
        if pipeline_resources.method == 'transform':
            return

        path = os.path.join(PLAYLIST_IMITATOR_PIPELINE_RESOURCES_DIR, PLAYLIST_IMITATOR_PIPELINE)

        with open(path, 'wb') as f:
            pickle.dump(pipeline_resources.pipeline, f)
