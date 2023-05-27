from abc import ABC
from typing import Dict, List, Optional

from flask import jsonify, Response
from flask_restful import Resource

from server.consts.api_consts import ACCESS_TOKEN, REFRESH_TOKEN, PLAYLIST_LINK_FORMAT
from server.consts.app_consts import ACCESS_CODE, IS_SUCCESS, PLAYLIST_LINK, PLAYLIST_DETAILS, MESSAGE
from server.data.playlist_creation_config import PlaylistCreationConfig
from server.data.query_condition import QueryCondition
from server.data.spotify_grant_type import SpotifyGrantType
from server.logic.access_token_generator import AccessTokenGenerator
from server.logic.data_filterer import DataFilterer
from server.logic.playlist_cover_photo_creator import PlaylistCoverPhotoCreator
from server.logic.playlists_creator import PlaylistsCreator
from server.utils import build_spotify_headers


class BaseContentController(Resource, ABC):
    def __init__(self):
        self._data_filterer = DataFilterer()
        self._playlists_creator = PlaylistsCreator()
        self._playlist_cover_photo_creator = PlaylistCoverPhotoCreator()

    def _generate_response(self, body: dict, uris: List[str], playlist_cover_prompt: Optional[str] = None) -> Response:
        if not uris:
            return self._build_no_content_response()

        config = PlaylistCreationConfig(
            access_code=body[ACCESS_CODE],
            playlist_details=body[PLAYLIST_DETAILS],
            grant_type=SpotifyGrantType.AUTHORIZATION_CODE,
            uris=uris
        )

        playlist_id = self._create_playlist(config, retries_left=2)
        if playlist_id is None:
            return self._build_authentication_failure_response()

        self._generate_playlist_cover(config.headers, playlist_id, playlist_cover_prompt)

        return jsonify(
            {
                IS_SUCCESS: True,
                PLAYLIST_LINK: PLAYLIST_LINK_FORMAT.format(playlist_id)
            }
        )

    def _create_playlist(self, config: PlaylistCreationConfig, retries_left: int) -> Optional[str]:
        if retries_left == 0:
            return

        try:
            return self._playlists_creator.create(config.uris, config.headers, config.playlist_details)

        except:
            config.access_code = config.access_token_generator_response[REFRESH_TOKEN]
            return self._create_playlist(config, retries_left=retries_left-1)

    def _generate_playlist_cover(self, headers: dict, playlist_id: str, playlist_cover_prompt: Optional[str]) -> None:
        if playlist_cover_prompt is None:
            return

        try:
            self._playlist_cover_photo_creator.put_playlist_cover(
                headers=headers,
                playlist_id=playlist_id,
                prompt=playlist_cover_prompt
            )
        except:
            print('Failed to create playlist cover')

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
