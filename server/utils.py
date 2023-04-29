from typing import Dict, List

from flask import Response, jsonify

from server.access_token_generator import AccessTokenGenerator
from server.playlists_generator import PlaylistsGenerator
from server.query_condition import QueryCondition

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
