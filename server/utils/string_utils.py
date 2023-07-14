import re

from dataclasses_json.stringcase import snakecase


def pre_process_column_name(column_name: str) -> str:
    snakecased_column_name = snakecase(column_name)
    return re.sub(r'min_|max_', '', snakecased_column_name)


def format_column_name(raw_column_name: str) -> str:
    return '_'.join([token.lower() for token in raw_column_name.split(' ')])


def titleize_feature_name(column_name: str) -> str:
    column_tokens = column_name.split('_')
    formatted_tokens = [column_token.capitalize() for column_token in column_tokens]

    return ' '.join(formatted_tokens)
