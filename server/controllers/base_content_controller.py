import json
from abc import ABC
from http import HTTPStatus
from typing import Dict, List, Optional

from flask import jsonify, Response
from flask_restful import Resource

from server.consts.api_consts import ACCESS_TOKEN, REFRESH_TOKEN
from server.consts.app_consts import ACCESS_CODE, IS_SUCCESS, PLAYLIST_LINK, PLAYLIST_DETAILS, MESSAGE
from server.consts.data_consts import URI
from server.data.playlist_creation_config import PlaylistCreationConfig
from server.data.query_condition import QueryCondition
from server.data.spotify_grant_type import SpotifyGrantType
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

        config = PlaylistCreationConfig(
            access_code=body[ACCESS_CODE],
            playlist_details=body[PLAYLIST_DETAILS],
            grant_type=SpotifyGrantType.AUTHORIZATION_CODE,
            uris=uris
        )

        playlist_link = self._create_playlist(config, retries_left=2)
        if playlist_link is None:
            return self._build_authentication_failure_response()

        return jsonify(
            {
                IS_SUCCESS: True,
                PLAYLIST_LINK: playlist_link
            }
        )

    def _create_playlist(self, config: PlaylistCreationConfig, retries_left: int) -> Optional[str]:
        if retries_left == 0:
            return

        response = AccessTokenGenerator.generate(config.access_code, config.grant_type)

        try:
            headers = self._build_request_headers(response)
            return self._playlists_creator.create(config.uris, headers, config.playlist_details)

        except:
            config.access_code = response[REFRESH_TOKEN]
            return self._create_playlist(config, retries_left=retries_left-1)

    @staticmethod
    def _build_request_headers(response: dict) -> Optional[Dict[str, str]]:
        bearer_token = response[ACCESS_TOKEN]

        if bearer_token is None:
            return

        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {bearer_token}"
        }

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
