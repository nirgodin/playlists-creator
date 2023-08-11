import json
from typing import List, Union, Optional

from aiohttp import ClientSession

from server.consts.prompt_consts import SERIALIZATION_ERROR_PROMPT_FORMAT
from server.logic.openai.openai_client import OpenAIClient


class OpenAIAdapter:
    def __init__(self, openai_client: OpenAIClient):
        self._openai_client = openai_client

    async def chat_completions(self,
                               prompt: str,
                               chat_history: Optional[List[dict]] = None,
                               retries_left: int = 3) -> Optional[Union[list, dict]]:
        if retries_left == 0:
            return

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
            return e.__str__()
