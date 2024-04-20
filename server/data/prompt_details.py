from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import dataclass_json

from server.data.query_condition import QueryCondition


@dataclass_json
@dataclass
class PromptDetails:
    musical_parameters: Optional[List[QueryCondition]]
    textual_parameters: Optional[str]
