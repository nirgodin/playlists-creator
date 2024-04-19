from abc import ABC, abstractmethod
from typing import Type

from genie_common.typing import Json

from server.consts.typing_consts import DataClass


class IPromptSerializer(ABC):
    @abstractmethod
    def build_prompt(self, user_text: str) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def model(self) -> Type[DataClass]:
        raise NotImplementedError

    @property
    @abstractmethod
    def response_type(self) -> Type[Json]:
        raise NotImplementedError
