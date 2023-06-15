import re

import numpy as np

YEAR_REGEX = re.compile(r'.*([1-3][0-9]{3})')


def extract_year(date: str) -> int:
    match = YEAR_REGEX.match(date)

    if match is not None:
        return int(match.group(1))

    return np.nan
