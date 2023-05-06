from dataclasses import dataclass
from typing import Any, Optional

from dataclasses_json import dataclass_json, LetterCase

from server.consts.openai_consts import IN_OPERATOR


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class QueryCondition:
    column: str
    operator: str
    value: Any
    include_nan: bool = False

    def __post_init__(self):
        self.condition = self._create_condition()

    def _create_condition(self) -> Optional[str]:
        if not self.value:
            return

        if self.operator == IN_OPERATOR:
            lowercased_values = [value.lower() for value in self.value]
            self.value = str(tuple(lowercased_values))

        condition = f'{self.column} {self.operator} {self.value}'

        if self.include_nan:
            condition += f' | {self.column}.isnull()'

        return condition
