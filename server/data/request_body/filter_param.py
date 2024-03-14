from dataclasses import dataclass
from typing import Union

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FilterParam:
    operator: str
    value: Union[list, float]
