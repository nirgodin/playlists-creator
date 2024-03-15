from dataclasses import dataclass
from typing import List, Any, Optional

from server.consts.data_consts import IN_OPERATOR, NUMERIC_OPERATORS
from server.data.column_group import ColumnGroup
from server.utils.data_utils import get_column_description
from server.utils.string_utils import titleize_feature_name


@dataclass
class ColumnDetails:
    name: str
    values: List[Any]
    group: ColumnGroup
    description: Optional[str] = None

    def __post_init__(self):
        self.formatted_name = titleize_feature_name(self.name)
        self.operator = IN_OPERATOR if self.group == ColumnGroup.POSSIBLE_VALUES else NUMERIC_OPERATORS

        if self.description is None:
            self.description = get_column_description(self.name)
