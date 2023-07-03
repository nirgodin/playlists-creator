from time import time


def get_current_timestamp() -> str:
    return str(round(time()))
