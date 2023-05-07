from abc import ABC
from typing import Dict, List

from flask import jsonify, Response
from flask_restful import Resource

from server.consts.app_consts import ACCESS_CODE, IS_SUCCESS, PLAYLIST_LINK, PLAYLIST_DETAILS
from server.consts.data_consts import URI
from server.data.query_condition import QueryCondition
from server.logic.access_token_generator import AccessTokenGenerator
from server.logic.data_filterer import DataFilterer
from server.logic.playlists_creator import PlaylistsCreator


class BaseContentController(Resource, ABC):
    def __init__(self):
        self._data_filterer = DataFilterer()
        self._playlists_creator = PlaylistsCreator()

    def _generate_response(self, body: dict, query_conditions: List[QueryCondition]) -> Response:
        headers = self._build_spotify_headers(body)
        playlist_details = body[PLAYLIST_DETAILS]
        playlist_link = self._generate(query_conditions, headers, playlist_details)
        res = {
            IS_SUCCESS: True,
            PLAYLIST_LINK: playlist_link
        }
        response = jsonify(res)

        return response

    def _generate(self, query_conditions: List[QueryCondition], headers: Dict[str, str], playlist_details: dict) -> str:
        filtered_data = self._data_filterer.filter(query_conditions)
        uris = filtered_data[URI].tolist()
        playlist_link = self._playlists_creator.create(uris, headers, playlist_details)

        return playlist_link

    @staticmethod
    def _build_spotify_headers(body: dict) -> Dict[str, str]:
        access_code = body[ACCESS_CODE]  # TODO: use .get instead
        bearer_token = AccessTokenGenerator.generate(access_code)

        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {bearer_token}"
        }
