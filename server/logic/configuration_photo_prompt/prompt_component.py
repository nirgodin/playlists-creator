from dataclasses import dataclass


@dataclass
class PromptComponent:
    name: str
    description: str
    param_type: str
