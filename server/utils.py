from functools import lru_cache
from typing import List

import pandas as pd
from pandas import DataFrame

from server.consts.data_consts import DATA_PATH


@lru_cache
def get_column_min_max_values(column_name: str) -> List[float]:
    data = load_data()
    formatted_column_name = format_column_name(column_name)
    min_value = float(data[formatted_column_name].min())
    max_value = float(data[formatted_column_name].max())

    return [min_value, max_value]


@lru_cache
def get_column_possible_values(column_name: str) -> List[str]:
    data = load_data()
    formatted_column_name = format_column_name(column_name)
    unique_values = data[formatted_column_name].unique().tolist()

    return sorted([str(value) for value in unique_values if not pd.isna(value)])


def format_column_name(raw_column_name: str) -> str:
    return '_'.join([token.lower() for token in raw_column_name.split(' ')])


def titleize_feature_name(column_name: str) -> str:
    column_tokens = column_name.split('_')
    formatted_tokens = [column_token.capitalize() for column_token in column_tokens]

    return ' '.join(formatted_tokens)


@lru_cache(maxsize=1)
def load_data() -> DataFrame:
    return pd.read_csv(DATA_PATH)
