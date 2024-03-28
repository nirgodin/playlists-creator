from typing import List, Dict

from genie_datastores.postgres.models import BaseORMModel
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql.elements import BinaryExpression

from server.utils.data_utils import get_columns_descriptions, get_possible_values_columns, get_orm_conditions_map


def test_all_possible_values_columns_have_descriptions():
    columns: List[str] = [column.key for column in get_possible_values_columns()]
    descriptions: Dict[str, str] = get_columns_descriptions()

    descriptions_columns_names = list(descriptions.keys())

    assert all(column in descriptions_columns_names for column in columns)


def test_no_column_duplicate_key():
    keys: List[str] = [column.key for column in get_possible_values_columns()]
    unique_keys = set(keys)

    assert sorted(keys) == sorted(unique_keys)


def test_all_possible_values_orms_have_condition_mapped():
    orms: List[BaseORMModel] = [column.class_ for column in get_possible_values_columns()]
    orm_conditions_map: Dict[BaseORMModel, List[BinaryExpression]] = get_orm_conditions_map()
    assert all(orm in orm_conditions_map.keys() for orm in orms)
