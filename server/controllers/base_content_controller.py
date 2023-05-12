import json
from abc import ABC
from http import HTTPStatus
from typing import Dict, List, Optional

from flask import jsonify, Response
from flask_restful import Resource

from server.consts.api_consts import ACCESS_TOKEN, REFRESH_TOKEN
from server.consts.app_consts import ACCESS_CODE, IS_SUCCESS, PLAYLIST_LINK, PLAYLIST_DETAILS, MESSAGE
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
        uris = self._data_filterer.filter(query_conditions)
        if not uris:
            return self._build_no_content_response()

        access_code = body[ACCESS_CODE]
        playlist_details = body[PLAYLIST_DETAILS]
        playlist_link = self._create_playlist(access_code, playlist_details, uris)
        if playlist_link is None:
            return self._build_authentication_failure_response()

        response = {
            IS_SUCCESS: True,
            PLAYLIST_LINK: playlist_link
        }

        return jsonify(response)

    def _create_playlist(self, access_code: str, playlist_details: dict, uris: List[str]) -> Optional[str]:  # TODO: Add retries
        response = AccessTokenGenerator.generate(access_code)
        bearer_token = response[ACCESS_TOKEN]

        if bearer_token is None:
            return

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {bearer_token}"
        }

        try:
            return self._playlists_creator.create(uris, headers, playlist_details)
        except:
            return self._create_playlist(response[REFRESH_TOKEN], playlist_details, uris)

    @staticmethod
    def _build_authentication_failure_response() -> Response:
        response = {
            IS_SUCCESS: False,
            MESSAGE: 'Could no authenticate your login details. Please re-enter and try again'
        }

        return jsonify(response)

    @staticmethod
    def _build_no_content_response() -> Response:
        response = {
            IS_SUCCESS: False,
            MESSAGE: 'Could not find any tracks that satisfy your request. Please retry another query'
        }

        return jsonify(response)
