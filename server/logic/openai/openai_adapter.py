import json
from copy import deepcopy
from typing import Union, Optional

from genie_common.models.openai import ChatCompletionsModel
from genie_common.openai import OpenAIClient
from genie_common.tools.logs import logger
from genie_common.typing import Json

from server.consts.openai_consts import CONTENT, ROLE, USER_ROLE, ASSISTANT_ROLE
from server.consts.prompt_consts import SERIALIZATION_ERROR_PROMPT_FORMAT
from server.data.chat_completions_request import ChatCompletionsRequest
from server.tools.case_progress_reporter import CaseProgressReporter


class OpenAIAdapter:
    def __init__(self, openai_client: OpenAIClient, case_progress_reporter: CaseProgressReporter):
        self._openai_client = openai_client
        self._case_progress_reporter = case_progress_reporter

    async def chat_completions(self, request: ChatCompletionsRequest) -> Optional[Json]:
        logger.info("Received chat_completions request")

        async with self._case_progress_reporter.report(case_id=request.case_id, status="prompt"):
            return await self._call_chat_completions_with_retries(request)

    async def _call_chat_completions_with_retries(self, request: ChatCompletionsRequest) -> Optional[Json]:
        if request.retries_left == 0:
            logger.warn("No retries left from chat_completions request. Returning None instead")
            return

        response: str = await self._openai_client.chat_completions.collect(
            messages=request.messages,
            model=ChatCompletionsModel.GPT_4
        )
        serialized_response = self._serialize_response(request, response)

        if isinstance(serialized_response, str):
            updated_request = self._update_request(
                request=request,
                response=response,
                error_message=serialized_response
            )
            return await self._call_chat_completions_with_retries(updated_request)

        return serialized_response

    def _serialize_response(self, request: ChatCompletionsRequest, response: str) -> Union[Json, str]:
        try:
            formatted_content = self._format_raw_openai_response(
                response=response,
                start_char=request.start_char,
                end_char=request.end_char
            )
            return json.loads(formatted_content)

        except Exception as e:
            logger.exception("Could not serialize OpenAI response to JSON. Retrying", extra={CONTENT: response})
            return e.__str__()

    @staticmethod
    def _format_raw_openai_response(response: str, start_char: str, end_char: str) -> str:
        prefix_split_content = response.split(start_char)
        if len(prefix_split_content) > 1:
            response = start_char.join(prefix_split_content[1:])

        suffix_split_content = response.split(end_char)
        if len(suffix_split_content) > 1:
            response = end_char.join(suffix_split_content[:-1])

        stripped_content = response.lstrip(start_char).rstrip(end_char)
        return f"{start_char}{stripped_content}{end_char}"

    @staticmethod
    def _update_request(request: ChatCompletionsRequest, response: str, error_message: str) -> ChatCompletionsRequest:
        updated_request = deepcopy(request)
        new_history = [
            {
                ROLE: ASSISTANT_ROLE,
                CONTENT: response
            },
            {
                ROLE: USER_ROLE,
                CONTENT: SERIALIZATION_ERROR_PROMPT_FORMAT.format(error_message=error_message)
            }
        ]
        updated_request.messages.extend(new_history)
        updated_request.retries_left -= 1

        return updated_request
