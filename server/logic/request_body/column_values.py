from dataclasses import dataclass
from typing import List, Any

from server.logic.request_body.column_group import ColumnGroup
from server.utils.string_utils import titleize_feature_name


@dataclass
class ColumnValues:
    name: str
    values: List[Any]
    group: ColumnGroup

    def __post_init__(self):
        self.formatted_name = titleize_feature_name(self.name)
