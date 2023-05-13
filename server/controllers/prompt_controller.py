from flask import Response, request

from server.consts.app_consts import PLAYLIST_DETAILS, PROMPT
from server.consts.openai_consts import PROMPT_PREFIX_FORMAT, PROMPT_SUFFIX_FORMAT
from server.controllers.base_content_controller import BaseContentController
from server.data.query_condition import QueryCondition
from server.logic.openai.columns_details_creator import ColumnsDetailsCreator
from server.logic.openai.openai_adapter import OpenAIAdapter
from server.utils import build_prompt


class PromptController(BaseContentController):
    def __init__(self):
        super().__init__()
        self._openai_adapter = OpenAIAdapter()
        self._columns_details_creator = ColumnsDetailsCreator()

    def post(self) -> Response:
        body = request.get_json()
        prompt = self._build_prompt(body)
        json_serialized_response = self._openai_adapter.fetch_openai(prompt)
        query_conditions = [QueryCondition.from_dict(condition) for condition in json_serialized_response]  # TODO: Add catch errors for cases where dict is not good

        return self._generate_response(body, query_conditions)

    def _build_prompt(self, body: dict) -> str:
        user_text = body[PLAYLIST_DETAILS][PROMPT]
        columns_details = self._columns_details_creator.create()
        prompt_prefix = PROMPT_PREFIX_FORMAT.format(columns_details=columns_details)
        prompt_suffix = PROMPT_SUFFIX_FORMAT.format(user_text=user_text)

        return build_prompt(prompt_prefix, prompt_suffix)
