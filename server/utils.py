from functools import lru_cache
from typing import Dict, List

import pandas as pd
from flask import Response, jsonify

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
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@lru_cache
def get_column_possible_values(column_name: str) -> list:
    data = pd.read_csv(r'groubyed_songs.csv')
    formatted_column_name = '_'.join([token.lower() for token in column_name.split(' ')])
    unique_values = data[formatted_column_name].unique().tolist()

    return sorted([value for value in unique_values if not pd.isna(value)])
