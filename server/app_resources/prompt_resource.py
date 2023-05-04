from flask import Response, request
from flask_restful import Resource

from server.logic.openai_adapter import OpenAIAdapter
from server.utils import generate_response


class Prompt(Resource):
    def __init__(self):
        self._openai_adapter = OpenAIAdapter()

    def post(self) -> Response:
        body = request.get_json()
        user_text = body['playlistDetails']['prompt']
        query_conditions = self._openai_adapter.generate_query_conditions(user_text)

        return generate_response(body, query_conditions)
