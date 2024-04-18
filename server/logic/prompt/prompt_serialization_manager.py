from typing import List, Optional, Type, Union

from genie_common.tools import logger
from genie_common.typing import Json

from server.consts.typing_consts import DataClass
from server.data.chat_completions_request import ChatCompletionsRequest
from server.logic.openai.openai_adapter import OpenAIAdapter
from server.logic.prompt.prompt_serializer_interface import IPromptSerializer
from server.utils.general_utils import to_dataclass


class PromptSerializationManager:
    def __init__(self,
                 prioritized_serializers: List[IPromptSerializer],
                 openai_adapter: OpenAIAdapter):
        self._prioritized_serializers = prioritized_serializers
        self._openai_adapter = openai_adapter

    async def serialize(self, user_text: str) -> DataClass:
        for serializer in self._prioritized_serializers:
            serialized_prompt = await self._apply_serializer(serializer, user_text)

            if serialized_prompt is not None:
                return serialized_prompt

    async def _apply_serializer(self, serializer: IPromptSerializer, user_text: str):
        prompt = serializer.serialize(user_text)
        request = ChatCompletionsRequest(
            prompt=prompt,
            expected_type=serializer.response_type
        )
        response: Optional[Json] = await self._openai_adapter.chat_completions(request)

        return self._serialize_openai_response(response, serializer.model)

    @staticmethod
    def _serialize_openai_response(response: Optional[Json],
                                   model: Type[DataClass]) -> Optional[Union[DataClass, List[DataClass]]]:
        try:
            if response is not None:
                return to_dataclass(response, model)

        except:
            logger.exception("Could not serialize OpenAI response to model. Returning None instead")
