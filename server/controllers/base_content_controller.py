import json
from abc import ABC
from http import HTTPStatus
from typing import Dict, List, Optional

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
        if headers is None:
            return self._build_authentication_failure_response()

        uris = self._data_filterer.filter(query_conditions)
        if not uris:
            return self._build_no_content_response()

        playlist_details = body[PLAYLIST_DETAILS]
        playlist_link = self._playlists_creator.create(uris, headers, playlist_details)
        response = {
            IS_SUCCESS: True,
            PLAYLIST_LINK: playlist_link
        }

        return jsonify(response)

    @staticmethod
    def _build_spotify_headers(body: dict) -> Optional[Dict[str, str]]:
        access_code = body[ACCESS_CODE]
        bearer_token = AccessTokenGenerator.generate(access_code)

        if bearer_token is not None:
            return {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {bearer_token}"
            }

    @staticmethod
    def _build_authentication_failure_response() -> Response:
        response = {
            IS_SUCCESS: False,
            PLAYLIST_LINK: ''
        }

        return Response(
            response=json.dumps(response),
            status=HTTPStatus.BAD_REQUEST,
            mimetype='application/json'
        )

    @staticmethod
    def _build_no_content_response() -> Response:
        response = {
            IS_SUCCESS: False,
            PLAYLIST_LINK: ''
        }

        return Response(
            response=json.dumps(response),
            status=HTTPStatus.NO_CONTENT,
            mimetype='application/json'
        )
