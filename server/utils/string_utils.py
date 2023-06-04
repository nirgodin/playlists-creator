import re

from dataclasses_json.stringcase import snakecase


def pre_process_column_name(column_name: str) -> str:
    snakecased_column_name = snakecase(column_name)
    return re.sub(r'min_|max_', '', snakecased_column_name)
