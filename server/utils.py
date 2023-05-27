import os.path
import random
from functools import lru_cache
from typing import List, Dict, Union

import pandas as pd
from PIL import Image
from pandas import DataFrame

from server.consts.api_consts import ACCESS_TOKEN
from server.consts.data_consts import DATA_PATH
from server.data.spotify_grant_type import SpotifyGrantType
from server.logic.access_token_generator import AccessTokenGenerator

BOOL_VALUES = [
    'false',
    'true'
]


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


def build_prompt(prompt_prefix: str, prompt_suffix: str) -> str:
    return f'{prompt_prefix}\n{prompt_suffix}'


def build_spotify_client_credentials_headers() -> Dict[str, str]:
    response = AccessTokenGenerator.generate(SpotifyGrantType.CLIENT_CREDENTIALS)
    access_token = response[ACCESS_TOKEN]

    return build_spotify_headers(access_token)


def build_spotify_headers(access_token: str) -> Dict[str, str]:
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }


def sample_list(n_candidates: int, n_selected_candidates: int) -> List[int]:
    return random.sample(range(0, n_candidates), n_selected_candidates)


def string_to_boolean(s: str) -> bool:
    return s.lower() == 'true'


def save_image_as_jpeg(image_path: str) -> str:
    original_file_extension = os.path.splitext(image_path)[-1]
    formatted_image_path = image_path.replace(original_file_extension, '.jpg')
    image = Image.open(image_path)
    rgb_image = image.convert('RGB')
    rgb_image.save(formatted_image_path)

    return formatted_image_path
