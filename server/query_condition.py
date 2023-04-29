from dataclasses import dataclass
from typing import Any, Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class QueryCondition:
    column: str
    operator: str
    value: Any

    def __post_init__(self):
        self.condition = self._create_condition()

    def _create_condition(self) -> Optional[str]:
        if not self.value:
            return

        if self.operator == 'in':
            lowercased_values = [value.lower() for value in self.value]
            self.value = str(tuple(lowercased_values))

        return f'{self.column} {self.operator} {self.value}'
