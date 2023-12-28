from dataclasses import dataclass
from typing import Any, Optional

from dataclasses_json import dataclass_json, LetterCase
from sqlalchemy import text
from sqlalchemy.sql.elements import TextClause

from server.consts.data_consts import IN_OPERATOR
from genie_common.utils import string_to_boolean
from server.consts.general_consts import BOOL_VALUES
from server.utils.postgres_utils import convert_iterable_to_postgres_format

ENUM_COLUMNS = "gender"


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class QueryCondition:
    column: str
    operator: str
    value: Any
    include_nan: bool = False

    def __post_init__(self):
        self.condition = self._create_condition()

    def _create_condition(self) -> Optional[TextClause]:  # TODO: Create using orm methods instead of plain text
        if not self.value:
            return

        self._format_value()
        condition = f'{self.column} {self.operator} {self.value}'

        # if self.include_nan:  # TODO: Think what to do with this
        #     condition += f' or {self.column} is null'

        return text(condition)

    def _format_value(self) -> None:
        if not self.operator == IN_OPERATOR:
            return

        formatted_values = []

        for sub_value in self.value:
            if sub_value.lower() in BOOL_VALUES:
                formatted_value = string_to_boolean(sub_value)
            elif self.column in ENUM_COLUMNS:
                formatted_value = sub_value.upper()
            else:
                formatted_value = sub_value

            formatted_values.append(formatted_value)

        self.value = convert_iterable_to_postgres_format(formatted_values)
