from typing import List, Optional, Union

from genie_common.tools import logger
from genie_common.typing import Json

from server.consts.typing_consts import DataClass
from server.data.chat_completions_request import ChatCompletionsRequest
from server.logic.openai.openai_adapter import OpenAIAdapter
from server.logic.prompt.prompt_serializer_interface import IPromptSerializer


class PromptSerializationManager:
    def __init__(self,
                 prioritized_serializers: List[IPromptSerializer],
                 openai_adapter: OpenAIAdapter):
        self._prioritized_serializers = prioritized_serializers
        self._openai_adapter = openai_adapter

    async def serialize(self, user_text: str) -> Optional[DataClass]:
        for serializer in self._prioritized_serializers:
            serialized_prompt = await self._apply_serializer(serializer, user_text)

            if serialized_prompt is not None:
                return serialized_prompt

        logger.warning("No serializer managed to serialize user text. Returning None instead")

    async def _apply_serializer(self, serializer: IPromptSerializer, user_text: str) -> Optional[Union[DataClass, List[DataClass]]]:
        prompt = serializer.build_prompt(user_text)
        request = ChatCompletionsRequest(
            prompt=prompt,
            expected_type=serializer.response_type
        )
        response: Optional[Json] = await self._openai_adapter.chat_completions(request)

        return self._serialize_openai_response(response, serializer)

    @staticmethod
    def _serialize_openai_response(response: Optional[Json],
                                   serializer: IPromptSerializer) -> Optional[Union[DataClass, List[DataClass]]]:
        try:
            if isinstance(response, dict) and serializer.response_type == dict:
                return serializer.model.from_dict(response)

            if isinstance(response, list) and serializer.response_type == list:
                return [serializer.model.from_dict(elem) for elem in response]

            logger.warning("Response type did not match expected type. Moving to next serializer")

        except:
            logger.exception("Could not serialize OpenAI response to model. Returning None instead")
