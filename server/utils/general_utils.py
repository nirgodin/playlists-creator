import os.path
import random
from functools import lru_cache, reduce
from typing import List, Dict

import pandas as pd

from server.consts.api_consts import ACCESS_TOKEN
from server.consts.path_consts import RESOURCES_DIR_PATH, DATA_PATH, COLUMNS_Z_SCORES_METADATA_PATH, \
    PLAYLIST_IMITATOR_DATABASE_PATH
from server.consts.env_consts import DATABASE_FOLDER_DRIVE_ID
from server.data.spotify_grant_type import SpotifyGrantType
from server.logic.access_token_generator import AccessTokenGenerator
from server.logic.configuration_photo_prompt.z_scores_metadata_creator import ZScoresMetadataCreator
from server.logic.playlist_imitation.playlist_imitator_database_creator import PlaylistImitatorDatabaseCreator
from server.tools.google_drive.google_drive_adapter import GoogleDriveAdapter
from server.utils.data_utils import load_data

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
    k = min(n_selected_candidates, n_candidates)
    return random.sample(range(0, n_candidates), k)


def string_to_boolean(s: str) -> bool:
    return s.lower() == 'true'


def download_database() -> None:
    if os.path.exists(DATA_PATH):
        return

    GoogleDriveAdapter().download_all_dir_files(
        folder_id=os.environ[DATABASE_FOLDER_DRIVE_ID],
        local_dir=RESOURCES_DIR_PATH
    )
    ZScoresMetadataCreator().create()
    PlaylistImitatorDatabaseCreator().create()


def chain_dicts(dicts: List[dict]) -> dict:
    return reduce(lambda dict1, dict2: {**dict1, **dict2}, dicts)
