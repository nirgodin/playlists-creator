from functools import lru_cache
from typing import Dict, List

import pandas as pd
from flask import Response, jsonify
from pandas import DataFrame

from server.consts.app_consts import PLAYLIST_DETAILS, ACCESS_CODE, IS_SUCCESS, PLAYLIST_LINK
from server.consts.data_consts import DATA_PATH
from server.logic.access_token_generator import AccessTokenGenerator
from server.logic.playlists_generator import PlaylistsGenerator
from server.data.query_condition import QueryCondition

playlists_generator = PlaylistsGenerator()


def build_spotify_headers(access_code: str) -> Dict[str, str]:
    bearer_token = AccessTokenGenerator.generate(access_code)
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {bearer_token}"
    }


def generate_response(body: dict, query_conditions: List[QueryCondition]) -> Response:
    access_code = body[ACCESS_CODE]
    playlist_details = body[PLAYLIST_DETAILS]
    playlist_link = playlists_generator.generate(query_conditions, access_code, playlist_details)
    res = {
        IS_SUCCESS: True,
        PLAYLIST_LINK: playlist_link
    }
    response = jsonify(res)

    return response


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


@lru_cache(maxsize=1)
def load_data() -> DataFrame:
    return pd.read_csv(DATA_PATH)
