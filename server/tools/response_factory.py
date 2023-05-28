from flask import Response, jsonify

from server.consts.api_consts import PLAYLIST_LINK_FORMAT
from server.consts.app_consts import IS_SUCCESS, MESSAGE, PLAYLIST_LINK


class ResponseFactory:
    @staticmethod
    def build_no_content_response() -> Response:
        response = {
            IS_SUCCESS: False,
            MESSAGE: 'Could not find any tracks that satisfy your request. Please retry another query'
        }

        return jsonify(response)

    @staticmethod
    def build_authentication_failure_response() -> Response:
        response = {
            IS_SUCCESS: False,
            MESSAGE: 'Could no authenticate your login details. Please re-enter and try again'
        }

        return jsonify(response)

    @staticmethod
    def build_success_response(playlist_id: str) -> Response:
        playlist_link = PLAYLIST_LINK_FORMAT.format(playlist_id)
        return jsonify(
            {
                IS_SUCCESS: True,
                PLAYLIST_LINK: playlist_link
            }
        )
