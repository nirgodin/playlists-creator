from functools import lru_cache
from typing import List, Tuple

import pandas as pd
from pandas import DataFrame, Series

from server.consts.data_consts import DEFAULT_OUTLIER_THRESHOLD, SERIES, Z_SCORE
from server.consts.path_consts import DATA_PATH
from server.utils.string_utils import format_column_name
from server.utils.statistics_utils import calculate_z_score


@lru_cache(maxsize=1)
def load_data() -> DataFrame:
    return pd.read_csv(DATA_PATH)


def sort_data_columns_alphabetically(data: DataFrame) -> DataFrame:
    sorted_columns = sorted(data.columns.tolist())
    return data[sorted_columns]


@lru_cache
def get_column_min_max_values(column_name: str, remove_outliers: bool = False) -> List[float]:
    data = load_data()
    formatted_column_name = format_column_name(column_name)

    if remove_outliers:
        min_value, max_value = get_series_non_outlier_min_max_values(data[formatted_column_name], outlier_threshold=3)
    else:
        min_value = float(data[formatted_column_name].min())
        max_value = float(data[formatted_column_name].max())

    return [min_value, max_value]


def get_series_non_outlier_min_max_values(series: Series,
                                          outlier_threshold: float = DEFAULT_OUTLIER_THRESHOLD) -> Tuple[float, float]:
    data = series.to_frame(SERIES)
    mean = data[SERIES].mean()
    std = data[SERIES].std()
    data[Z_SCORE] = data[SERIES].apply(lambda x: abs(calculate_z_score(x, mean, std)))
    non_outlier_data = data[data[Z_SCORE] < outlier_threshold][SERIES]

    return float(non_outlier_data.min()), float(non_outlier_data.max())


@lru_cache
def get_column_possible_values(column_name: str) -> List[str]:
    data = load_data()
    formatted_column_name = format_column_name(column_name)
    unique_values = data[formatted_column_name].unique().tolist()

    return sorted([str(value) for value in unique_values if not pd.isna(value)])
