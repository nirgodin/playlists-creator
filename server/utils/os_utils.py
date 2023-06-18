import os


def is_empty_dir(dir_path: str) -> bool:
    dir_files = os.listdir(dir_path)
    return len(dir_files) == 0
