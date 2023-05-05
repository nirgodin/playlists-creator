import json
import os
from typing import List, Union, Optional

import openai

from server.consts.openai_consts import SERIALIZATION_ERROR_PROMPT_FORMAT
from server.data.query_condition import QueryCondition
from server.logic.openai.prompt_builder import PromptBuilder


class OpenAIAdapter:
    def __init__(self):
        openai.api_key = os.environ['OPENAI_API_KEY']
        self._openai_model = openai.ChatCompletion()
        self._prompt_build = PromptBuilder()

    def generate_query_conditions(self,
                                  user_text: str,
                                  chat_history: Optional[List[dict]] = None,
                                  retries_left: int = 3) -> Optional[List[QueryCondition]]:
        if retries_left == 0:
            return

        prompt = self._prompt_build.build(user_text)
        messages = self._build_request_messages(prompt, chat_history)
        response = self._openai_model.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        response_content = response.choices[0].message.content
        serialized_response = self._wrap_serialize_response(response_content)

        if isinstance(serialized_response, list):
            return serialized_response
        else:
            new_history = [
                {
                    "role": "assistant",
                    "content": serialized_response
                },
                {
                    "role": "user",
                    "content": SERIALIZATION_ERROR_PROMPT_FORMAT.format(error_message=serialized_response)
                }
            ]
            chat_history.extend(new_history)
            return self.generate_query_conditions(user_text, chat_history, retries_left - 1)

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

    def _wrap_serialize_response(self, response_content: str) -> Union[List[QueryCondition], str]:
        try:
            return self._serialize_response(response_content)
        except Exception as e:
            return e.__str__()

    @staticmethod
    def _serialize_response(response_content: str) -> List[QueryCondition]:
        json_serialized_response = json.loads(response_content)
        return [QueryCondition.from_dict(condition) for condition in json_serialized_response]


if __name__ == '__main__':
    text = 'playlist of songs in english in high tempo, but not very popular songs'
    OpenAIAdapter().generate_query_conditions(text)
