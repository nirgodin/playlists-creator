from typing import Type

from server.consts.prompt_consts import QUERY_CONDITIONS_PROMPT_PREFIX_FORMAT, QUERY_CONDITIONS_PROMPT_SUFFIX_FORMAT
from server.data.prompt_details import PromptDetails
from server.logic.prompt.prompt_serializer_interface import IPromptSerializer
from server.utils.general_utils import build_prompt


class QueryConditionsPromptSerializer(IPromptSerializer):
    def __init__(self, columns_details: str):
        self._columns_details = columns_details

    def serialize(self, user_text: str) -> str:
        prompt_prefix = QUERY_CONDITIONS_PROMPT_PREFIX_FORMAT.format(columns_details=self._columns_details)
        prompt_suffix = QUERY_CONDITIONS_PROMPT_SUFFIX_FORMAT.format(user_text=user_text)

        return build_prompt(prompt_prefix, prompt_suffix)

    @property
    def model(self) -> Type[PromptDetails]:
        return PromptDetails

    @property
    def response_type(self) -> Type[dict]:
        return dict
