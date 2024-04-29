import os.path
import random
from typing import List

from genie_common.tools import logger
from genie_datastores.google.drive import GoogleDriveClient

from server.consts.env_consts import DATABASE_FOLDER_DRIVE_ID, TRACK_NAMES_EMBEDDINGS_FOLDER_DRIVE_ID
from server.consts.path_consts import RESOURCES_DIR_PATH, DATA_PATH, TRACK_NAMES_EMBEDDINGS_PATH


def build_prompt(prompt_prefix: str, prompt_suffix: str) -> str:
    return f'{prompt_prefix}\n{prompt_suffix}'


def sample_list(n_candidates: int, n_selected_candidates: int) -> List[int]:
    k = min(n_selected_candidates, n_candidates)
    return random.sample(range(0, n_candidates), k)


def download_database() -> None:
    db_drive_id = os.getenv(DATABASE_FOLDER_DRIVE_ID)

    if db_drive_id is None:
        logger.warn("Did not find `DATABASE_FOLDER_DRIVE_ID` env var. Aborting database download")
        return

    drive_client = GoogleDriveClient.create()

    if not os.path.exists(DATA_PATH):
        drive_client.download_all_dir_files(
            folder_id=db_drive_id,
            local_dir=RESOURCES_DIR_PATH
        )

    if not os.path.exists(TRACK_NAMES_EMBEDDINGS_PATH):
        drive_client.download_all_dir_files(
            folder_id=os.environ[TRACK_NAMES_EMBEDDINGS_FOLDER_DRIVE_ID],
            local_dir=RESOURCES_DIR_PATH
        )
