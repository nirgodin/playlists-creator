from dataclasses import dataclass
from typing import Type

from genie_common.typing import Json

from server.consts.openai_consts import CONTENT, ROLE, USER_ROLE


@dataclass
class ChatCompletionsRequest:
    prompt: str
    expected_type: Type[Json]
    retries_left: int = 1

    def __post_init__(self):
        self.messages = [
            {
                ROLE: USER_ROLE,
                CONTENT: self.prompt
            }
        ]
