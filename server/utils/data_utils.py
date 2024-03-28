import json
from functools import lru_cache
from typing import Tuple, List, Dict

import pandas as pd
from genie_datastores.postgres.models import BaseORMModel, AudioFeatures, Artist, SpotifyTrack, TrackLyrics, RadioTrack
from pandas import DataFrame, Series
from sqlalchemy.sql.elements import BinaryExpression

from server.consts.data_consts import DEFAULT_OUTLIER_THRESHOLD, SERIES, Z_SCORE
from server.consts.path_consts import DATA_PATH, COLUMNS_DESCRIPTIONS_PATH
from server.utils.statistics_utils import calculate_z_score


@lru_cache(maxsize=1)
def load_data() -> DataFrame:
    return pd.read_csv(DATA_PATH)


def sort_data_columns_alphabetically(data: DataFrame) -> DataFrame:
    sorted_columns = sorted(data.columns.tolist())
    return data[sorted_columns]


def get_series_non_outlier_min_max_values(series: Series,
                                          outlier_threshold: float = DEFAULT_OUTLIER_THRESHOLD) -> Tuple[float, float]:
    data = series.to_frame(SERIES)
    mean = data[SERIES].mean()
    std = data[SERIES].std()
    data[Z_SCORE] = data[SERIES].apply(lambda x: abs(calculate_z_score(x, mean, std)))
    non_outlier_data = data[data[Z_SCORE] < outlier_threshold][SERIES]

    return float(non_outlier_data.min()), float(non_outlier_data.max())


@lru_cache
def get_column_description(column_name: str) -> str:
    columns_descriptions = get_columns_descriptions()
    return columns_descriptions[column_name]


@lru_cache
def get_columns_descriptions() -> dict:
    with open(COLUMNS_DESCRIPTIONS_PATH) as f:
        return json.load(f)


@lru_cache
def get_possible_values_columns() -> List[BaseORMModel]:
    return [  # TODO: Think how to add popularity, followers, main_genre, radio_play_count, release_year
        AudioFeatures.acousticness,
        Artist.gender,
        AudioFeatures.danceability,
        AudioFeatures.duration_ms,  # TODO: Think how to transform to minutes
        AudioFeatures.energy,
        SpotifyTrack.explicit,
        AudioFeatures.instrumentalness,
        Artist.is_israeli,
        AudioFeatures.key,
        TrackLyrics.language,
        AudioFeatures.liveness,
        AudioFeatures.loudness,
        AudioFeatures.mode,
        AudioFeatures.tempo,
        AudioFeatures.time_signature,
        SpotifyTrack.number,
        AudioFeatures.valence
    ]


@lru_cache
def get_orm_conditions_map() -> Dict[BaseORMModel, List[BinaryExpression]]:
    return {
        SpotifyTrack: [RadioTrack.track_id == SpotifyTrack.id],
        AudioFeatures: [RadioTrack.track_id == AudioFeatures.id],
        Artist: [RadioTrack.track_id == SpotifyTrack.id, SpotifyTrack.artist_id == Artist.id],
        TrackLyrics: [RadioTrack.track_id == TrackLyrics.id]
    }
