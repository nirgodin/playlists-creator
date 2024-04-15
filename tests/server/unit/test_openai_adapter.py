import json
from logging import ERROR, WARNING
from random import choice

import pytest
from _pytest.logging import LogCaptureFixture
from aioresponses import aioresponses
from genie_common.typing import Json
from genie_common.utils import random_alphanumeric_string, random_string_dict, random_string_array

from server.data.chat_completions_request import ChatCompletionsRequest
from server.logic.openai.openai_adapter import OpenAIAdapter
from tests.server.utils import assert_expected_level_logs_count, build_chat_completions_response


class TestOpenAIAdapter:
    @pytest.mark.parametrize("message_content", [random_string_dict(), random_string_array()])
    async def test_chat_completions__valid_response(self,
                                                    message_content: Json,
                                                    openai_adapter: OpenAIAdapter,
                                                    mock_responses: aioresponses):
        self._given_valid_response(mock_responses, message_content)
        request = ChatCompletionsRequest(
            prompt=random_alphanumeric_string(),
            expected_type=type(message_content)
        )

        actual = await openai_adapter.chat_completions(request)

        assert actual == message_content

    @pytest.mark.parametrize("message_content", [random_string_dict(), random_string_array()])
    async def test_chat_completions__valid_response_with_retry(self,
                                                               message_content: Json,
                                                               openai_adapter: OpenAIAdapter,
                                                               mock_responses: aioresponses,
                                                               caplog: LogCaptureFixture):
        self._given_first_response_invalid_second_valid(mock_responses, message_content)
        request = ChatCompletionsRequest(
            prompt=random_alphanumeric_string(),
            expected_type=type(message_content),
            retries_left=2
        )

        with caplog.at_level(ERROR):
            actual = await openai_adapter.chat_completions(request)

        assert actual == message_content
        assert len(caplog.records) == 1

    async def test_chat_completions__invalid_response__returns_none(self,
                                                                    openai_adapter: OpenAIAdapter,
                                                                    mock_responses: aioresponses,
                                                                    caplog: LogCaptureFixture):
        self._given_invalid_response(mock_responses)
        request = ChatCompletionsRequest(
            prompt=random_alphanumeric_string(),
            expected_type=choice([list, dict]),
        )

        with caplog.at_level(WARNING):
            actual = await openai_adapter.chat_completions(request)

        assert actual is None
        assert_expected_level_logs_count(caplog, level="WARNING", expected=1)
        assert_expected_level_logs_count(caplog, level="ERROR", expected=1)

    @staticmethod
    def _given_valid_response(mock_responses: aioresponses, message_content: Json) -> None:
        jsonified_content = json.dumps(message_content)
        dirty_jsonified_content = f"{random_alphanumeric_string()}{jsonified_content}{random_alphanumeric_string()}"

        mock_responses.post(
            url="https://api.openai.com/v1/chat/completions",
            payload=build_chat_completions_response(dirty_jsonified_content)
        )

    @staticmethod
    def _given_invalid_response(mock_responses: aioresponses) -> None:
        content = random_alphanumeric_string()
        mock_responses.post(
            url="https://api.openai.com/v1/chat/completions",
            payload=build_chat_completions_response(content)
        )

    def _given_first_response_invalid_second_valid(self, mock_responses: aioresponses, message_content: Json) -> None:
        self._given_invalid_response(mock_responses)
        self._given_valid_response(mock_responses, message_content)
