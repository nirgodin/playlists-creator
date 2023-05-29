from abc import ABC, abstractmethod
from typing import Optional, List

from flask import request, Request, Response, jsonify
from flask_restful import Resource

from server.consts.app_consts import IS_SUCCESS, MESSAGE, ACCESS_CODE, PLAYLIST_DETAILS
from server.data.playlist_creation_config import PlaylistCreationConfig
from server.data.spotify_grant_type import SpotifyGrantType
from server.logic.playlist_cover_photo_creator import PlaylistCoverPhotoCreator
from server.logic.playlists_creator import PlaylistsCreator
from server.tools.response_factory import ResponseFactory


class BaseContentController(Resource, ABC):
    def __init__(self):
        self._playlists_creator = PlaylistsCreator()
        self._playlist_cover_photo_creator = PlaylistCoverPhotoCreator()

    def post(self):
        request_body = self._get_request_body(request)

        uris = self._generate_tracks_uris(request_body)
        if not uris:
            return ResponseFactory.build_no_content_response()

        playlist_id = self._create_playlist(request_body, uris)
        if playlist_id is None:
            return ResponseFactory.build_authentication_failure_response()

        return ResponseFactory.build_success_response(playlist_id)

    @abstractmethod
    def _get_request_body(self, client_request: Request) -> dict:
        raise NotImplementedError

    @abstractmethod
    def _generate_tracks_uris(self, request_body: dict) -> Optional[List[str]]:
        raise NotImplementedError

    @abstractmethod
    def _generate_playlist_cover_prompt(self, request_body: dict) -> str:
        raise NotImplementedError

    def _create_playlist(self, request_body: dict, uris: List[str]) -> Optional[str]:
        config = PlaylistCreationConfig(
            access_code=request_body[ACCESS_CODE],
            playlist_details=request_body[PLAYLIST_DETAILS],
            grant_type=SpotifyGrantType.AUTHORIZATION_CODE,
            uris=uris
        )
        playlist_id = self._playlists_creator.create(config, retries_left=1)

        if playlist_id is None:
            return

        self._create_playlist_cover(request_body, playlist_id, config.headers)

        return playlist_id

    def _create_playlist_cover(self, request_body: dict, playlist_id: str, headers: dict) -> None:
        try:
            prompt = self._generate_playlist_cover_prompt(request_body)
            self._playlist_cover_photo_creator.put_playlist_cover(
                headers=headers,
                playlist_id=playlist_id,
                prompt=prompt
            )

        except:
            print('Failed to create playlist cover')
