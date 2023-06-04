from flask import Response, jsonify
from flask_restful import Resource

from server.consts.app_consts import FILTER_PARAMS, ACCESS_CODE, PLAYLIST_DETAILS, PLAYLIST_NAME, PLAYLIST_DESCRIPTION, \
    IS_PUBLIC, PROMPT, REQUEST_BODY
from server.logic.default_filter_params_generator import DefaultFilterParamsGenerator


class RequestBodyController(Resource):
    def __init__(self):
        self._default_filter_params_generator = DefaultFilterParamsGenerator()

    def get(self) -> Response:
        body = {
            FILTER_PARAMS: self._default_filter_params_generator.get_filter_params_defaults(),
            ACCESS_CODE: '',
            PLAYLIST_DETAILS: {
                PLAYLIST_NAME: '',
                PLAYLIST_DESCRIPTION: '',
                IS_PUBLIC: False,
                PROMPT: ''
            }
        }
        response = {
            REQUEST_BODY: [body]
        }

        return jsonify(response)
