from dataclasses import dataclass
from typing import Any, Optional

from dataclasses_json import dataclass_json, LetterCase

from server.consts.data_consts import IN_OPERATOR
from server.utils.general_utils import string_to_boolean
from server.consts.general_consts import BOOL_VALUES


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

        self._format_value()
        condition = f'{self.column} {self.operator} {self.value}'

        if self.include_nan:
            condition += f' | {self.column}.isnull()'

        return condition

    def _format_value(self) -> None:
        if not self.operator == IN_OPERATOR:
            return

        formatted_values = []

        for sub_value in self.value:
            if sub_value.lower() in BOOL_VALUES:
                formatted_value = string_to_boolean(sub_value)
            else:
                formatted_value = sub_value

            formatted_values.append(formatted_value)

        self.value = str(tuple(formatted_values))
