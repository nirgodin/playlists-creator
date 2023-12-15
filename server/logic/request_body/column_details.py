from dataclasses import dataclass
from typing import List, Any

from server.consts.data_consts import IN_OPERATOR, NUMERIC_OPERATORS
from server.logic.request_body.column_group import ColumnGroup
from server.utils.data_utils import get_column_description
from server.utils.string_utils import titleize_feature_name


@dataclass
class ColumnDetails:
    name: str
    values: List[Any]
    group: ColumnGroup

    def __post_init__(self):
        self.formatted_name = titleize_feature_name(self.name)
        self.description = get_column_description(self.name)
        self.operator = IN_OPERATOR if self.group == ColumnGroup.POSSIBLE_VALUES else NUMERIC_OPERATORS
