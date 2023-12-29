import json
from typing import List, Union, Optional

from genie_common.models.openai import ChatCompletionsModel
from genie_common.openai import OpenAIClient

from server.consts.app_consts import PROMPT
from server.consts.openai_consts import CONTENT
from server.consts.prompt_consts import SERIALIZATION_ERROR_PROMPT_FORMAT
from genie_common.tools.logs import logger


class OpenAIAdapter:  # TODO: Should be refactored
    def __init__(self, openai_client: OpenAIClient):
        self._openai_client = openai_client

    async def chat_completions(self,
                               prompt: str,
                               start_char: str,
                               end_char: str,
                               chat_history: Optional[List[dict]] = None,
                               retries_left: int = 3) -> Optional[Union[list, dict]]:
        if retries_left == 0:
            logger.info("No retries left from chat_completions request. Returning None instead", extra={PROMPT: prompt})
            return

        logger.info("Received chat_completions request", extra={PROMPT: prompt, "retries_left": retries_left})
        chat_history = self._build_request_messages(prompt, chat_history)
        response_content = await self._openai_client.chat_completions.collect(
            messages=chat_history,
            model=ChatCompletionsModel.GPT_4
        )
        serialized_response = self._serialize_response(response_content, start_char, end_char)

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
            return await self.chat_completions(
                prompt=prompt,
                start_char=start_char,
                end_char=end_char,
                chat_history=chat_history,
                retries_left=retries_left - 1
            )

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

    def _serialize_response(self, response_content: str, start_char: str, end_char: str) -> Union[list, dict, str]:
        try:
            formatted_content = self._format_raw_openai_response(response_content, start_char, end_char)
            return json.loads(formatted_content)

        except Exception as e:
            logger.exception("Could not serialize OpenAI response to JSON. Retrying", extra={CONTENT: response_content})
            return e.__str__()

    @staticmethod
    def _format_raw_openai_response(response_content: str, start_char: str, end_char: str) -> str:
        prefix_split_content = response_content.split(start_char)
        if len(prefix_split_content) > 1:
            response_content = start_char.join(prefix_split_content[1:])

        suffix_split_content = response_content.split(end_char)
        if len(suffix_split_content) > 1:
            response_content = end_char.join(suffix_split_content[:-1])

        stripped_content = response_content.lstrip(start_char).rstrip(end_char)
        return f"{start_char}{stripped_content}{end_char}"
