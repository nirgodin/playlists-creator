from functools import lru_cache
from typing import Dict, List

import pandas as pd
from flask import Response, jsonify
from pandas import DataFrame

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
    access_code = body['accessCode']
    playlist_details = body['playlistDetails']
    playlists_generator.generate(query_conditions, access_code, playlist_details)
    res = {
        'isSuccess': True
    }
    response = jsonify(res)

    return response


def format_column_name(raw_column_name: str) -> str:
    return '_'.join([token.lower() for token in raw_column_name.split(' ')])


@lru_cache(maxsize=1)
def load_data() -> DataFrame:
    return pd.read_csv(r'groubyed_songs.csv')
