from dataclasses import dataclass
from typing import List


@dataclass
class ColumnDetails:
    index: int
    name: str
    operator: str
    values: List[str]
