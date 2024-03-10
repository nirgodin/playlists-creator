from typing import List, Dict

from server.component_factory import get_possible_values_columns
from server.utils.data_utils import get_columns_descriptions


def test_all_possible_values_columns_have_descriptions():
    columns: List[str] = [column.key for column in get_possible_values_columns()]
    descriptions: Dict[str, str] = get_columns_descriptions()

    descriptions_columns_names = list(descriptions.keys())

    assert all(column in descriptions_columns_names for column in columns)
