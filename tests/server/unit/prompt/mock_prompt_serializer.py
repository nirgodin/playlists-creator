from dataclasses import dataclass
from typing import Type

from dataclasses_json import dataclass_json
from genie_common.typing import Json

from server.logic.prompt.prompt_serializer_interface import IPromptSerializer


@dataclass_json
@dataclass
class MockSerializationModel:
    value: str


class MockPromptSerializer(IPromptSerializer):
    def __init__(self, prompt_prefix: str, response_type: Type[Json]):
        self._prompt_prefix = prompt_prefix
        self._response_type = response_type

    def build_prompt(self, user_text: str) -> str:
        return f"{self._prompt_prefix}{user_text}"

    @property
    def model(self) -> Type[MockSerializationModel]:
        return MockSerializationModel

    @property
    def response_type(self) -> Type[Json]:
        return self._response_type
