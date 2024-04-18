from logging import WARNING
from typing import Dict, List
from unittest.mock import AsyncMock, call, _Call

from _pytest.fixtures import fixture
from _pytest.logging import LogCaptureFixture
from genie_common.utils import random_alphanumeric_string, random_string_dict

from server.data.chat_completions_request import ChatCompletionsRequest
from server.logic.openai.openai_adapter import OpenAIAdapter
from server.logic.prompt.prompt_serialization_manager import PromptSerializationManager
from tests.server.unit.prompt.mock_prompt_serializer import MockPromptSerializer, MockSerializationModel


class TestPromptSerializationManager:
    async def test_serialize__list_serializer_success__returns_list(
            self,
            mock_openai_adapter: AsyncMock,
            user_text: str,
            serialization_manager: PromptSerializationManager,
            expected_list_chat_request: call
    ):
        response = [self._random_mock_serialization_model_response() for _ in range(1, 5)]
        mock_openai_adapter.chat_completions.return_value = response
        expected = [MockSerializationModel.from_dict(e) for e in response]

        actual = await serialization_manager.serialize(user_text)

        mock_openai_adapter.chat_completions.assert_has_calls([expected_list_chat_request])
        assert actual == expected

    async def test_serialize__list_serializer_failure_dict_serializer_success__returns_dict(
            self,
            mock_openai_adapter: AsyncMock,
            user_text: str,
            serialization_manager: PromptSerializationManager,
            caplog: LogCaptureFixture,
            expected_chat_requests: List[_Call]
    ):
        response = self._random_mock_serialization_model_response()
        mock_openai_adapter.chat_completions.return_value = response
        expected = MockSerializationModel.from_dict(response)

        with caplog.at_level(WARNING):
            actual = await serialization_manager.serialize(user_text)

        mock_openai_adapter.chat_completions.assert_has_calls(expected_chat_requests)
        assert actual == expected
        assert caplog.messages == ["Response type did not match expected type. Moving to next serializer"]

    async def test_serialize__both_serializers_fail__returns_none(
            self,
            mock_openai_adapter: AsyncMock,
            user_text: str,
            serialization_manager: PromptSerializationManager,
            caplog: LogCaptureFixture,
            expected_chat_requests: List[_Call]
    ):
        mock_openai_adapter.chat_completions.return_value = random_string_dict()

        with caplog.at_level(WARNING):
            actual = await serialization_manager.serialize(user_text)

        mock_openai_adapter.chat_completions.assert_has_calls(expected_chat_requests)
        assert actual is None
        assert caplog.messages == [
            "Response type did not match expected type. Moving to next serializer",
            "Could not serialize OpenAI response to model. Returning None instead",
            "No serializer managed to serialize user text. Returning None instead"
        ]

    @fixture(scope="function")
    def serialization_manager(self, mock_openai_adapter: AsyncMock, prompt_prefix: str) -> PromptSerializationManager:
        return PromptSerializationManager(
            openai_adapter=mock_openai_adapter,
            prioritized_serializers=[
                MockPromptSerializer(prompt_prefix=prompt_prefix, response_type=list),
                MockPromptSerializer(prompt_prefix=prompt_prefix, response_type=dict)
            ]
        )

    @fixture(scope="class")
    def prompt_prefix(self) -> str:
        return random_alphanumeric_string()

    @fixture(scope="class")
    def user_text(self) -> str:
        return random_alphanumeric_string()

    @fixture(scope="function")
    def mock_openai_adapter(self) -> AsyncMock:
        return AsyncMock(OpenAIAdapter)

    @fixture(scope="class")
    def expected_chat_requests(self,
                               expected_list_chat_request: _Call,
                               expected_dict_chat_request: _Call) -> List[_Call]:
        return [expected_list_chat_request, expected_dict_chat_request]

    @fixture(scope="class")
    def expected_list_chat_request(self, prompt_prefix: str, user_text: str) -> _Call:
        request = ChatCompletionsRequest(
            prompt=f"{prompt_prefix}{user_text}",
            expected_type=list,
        )
        return call(request)

    @fixture(scope="class")
    def expected_dict_chat_request(self, prompt_prefix: str, user_text: str) -> _Call:
        request = ChatCompletionsRequest(
            prompt=f"{prompt_prefix}{user_text}",
            expected_type=dict,
        )
        return call(request)

    @staticmethod
    def _random_mock_serialization_model_response() -> Dict[str, str]:
        return {"value": random_alphanumeric_string()}
