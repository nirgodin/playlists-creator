from functools import lru_cache

import pandas as pd
from pandas import DataFrame

from server.consts.path_consts import DATA_PATH


@lru_cache(maxsize=1)
def load_data() -> DataFrame:
    return pd.read_csv(DATA_PATH)


def sort_data_columns_alphabetically(data: DataFrame) -> DataFrame:
    sorted_columns = sorted(data.columns.tolist())
    return data[sorted_columns]
