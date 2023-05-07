from flask import Response, request

from server.consts.app_consts import PLAYLIST_DETAILS, PROMPT
from server.controllers.base_content_controller import BaseContentController
from server.logic.openai.openai_adapter import OpenAIAdapter


class PromptController(BaseContentController):
    def __init__(self):
        super().__init__()
        self._openai_adapter = OpenAIAdapter()

    def post(self) -> Response:
        body = request.get_json()
        user_text = body[PLAYLIST_DETAILS][PROMPT]
        query_conditions = self._openai_adapter.generate_query_conditions(user_text)

        return self._generate_response(body, query_conditions)
