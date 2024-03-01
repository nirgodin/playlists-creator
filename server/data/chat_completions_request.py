from dataclasses import dataclass

from server.consts.openai_consts import CONTENT, ROLE, USER_ROLE


@dataclass
class ChatCompletionsRequest:
    case_id: str
    prompt: str
    start_char: str
    end_char: str
    retries_left: int = 3

    def __post_init__(self):
        self.messages = [
            {
                ROLE: USER_ROLE,
                CONTENT: self.prompt
            }
        ]
