from typing import Iterable


def convert_iterable_to_postgres_format(iterable: Iterable) -> str:
    formatted_values = []

    for elem in iterable:
        if isinstance(elem, str):
            formatted_values.append(f"'{elem}'")
        else:
            formatted_values.append(str(elem))

    joined_values = ",".join(formatted_values)
    return f"({joined_values})"
