from dataclasses import dataclass
from typing import Any

from dataclasses_json import dataclass_json, LetterCase
from genie_common.utils import string_to_boolean

from server.consts.data_consts import IN_OPERATOR
from server.consts.general_consts import BOOL_VALUES, STRING_LOWER_BOOL_VALUES

ENUM_COLUMNS = ["gender"]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class QueryCondition:
    column: str
    operator: str
    value: Any

    def __post_init__(self):
        self._format_value()

    def _format_value(self) -> None:
        if self.operator == IN_OPERATOR and not isinstance(self.value, list):
            self.value = [self.value]

        if not self.operator == IN_OPERATOR:
            return

        formatted_values = []

        for sub_value in self.value:
            if sub_value in BOOL_VALUES:
                formatted_value = sub_value
            elif sub_value.lower() in STRING_LOWER_BOOL_VALUES:
                formatted_value = string_to_boolean(sub_value)
            elif self.column in ENUM_COLUMNS:
                formatted_value = sub_value.upper()
            else:
                formatted_value = sub_value

            formatted_values.append(formatted_value)

        self.value = formatted_values
