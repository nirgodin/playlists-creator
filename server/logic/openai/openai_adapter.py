import json
from typing import List, Union, Optional

from server.consts.app_consts import PROMPT
from server.consts.openai_consts import CONTENT
from server.consts.prompt_consts import SERIALIZATION_ERROR_PROMPT_FORMAT
from server.logic.openai.openai_client import OpenAIClient
from genie_common.tools.logs import logger


class OpenAIAdapter:
    def __init__(self, openai_client: OpenAIClient):
        self._openai_client = openai_client

    async def chat_completions(self,
                               prompt: str,
                               chat_history: Optional[List[dict]] = None,
                               retries_left: int = 3) -> Optional[Union[list, dict]]:
        if retries_left == 0:
            logger.info("No retries left from chat_completions request. Returning None instead", extra={PROMPT: prompt})
            return

        logger.info("Received chat_completions request", extra={PROMPT: prompt, "retries_left": retries_left})
        chat_history = self._build_request_messages(prompt, chat_history)
        response_content = await self._openai_client.chat_completions(chat_history)
        serialized_response = self._serialize_response(response_content)

        if not isinstance(serialized_response, str):
            return serialized_response
        else:
            new_history = [
                {
                    "role": "assistant",
                    "content": response_content
                },
                {
                    "role": "user",
                    "content": SERIALIZATION_ERROR_PROMPT_FORMAT.format(error_message=serialized_response)
                }
            ]
            chat_history.extend(new_history)
            return await self.chat_completions(prompt, chat_history, retries_left - 1)

    @staticmethod
    def _build_request_messages(prompt: str, chat_history: Optional[List[dict]]) -> List[dict]:
        if chat_history is None:
            return [
                {
                    "role": "user",
                    "content": prompt
                }
            ]

        return chat_history

    @staticmethod
    def _serialize_response(response_content: str) -> Union[list, dict, str]:
        try:
            return json.loads(response_content)

        except Exception as e:
            logger.exception("Could not serialize OpenAI response to JSON. Retrying", extra={CONTENT: response_content})
            return e.__str__()
