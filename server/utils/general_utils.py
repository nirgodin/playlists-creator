import os.path
import random
from typing import List, Union, Type

from genie_datastores.google.drive import GoogleDriveClient

from server.consts.env_consts import DATABASE_FOLDER_DRIVE_ID, TRACK_NAMES_EMBEDDINGS_FOLDER_DRIVE_ID
from server.consts.path_consts import RESOURCES_DIR_PATH, DATA_PATH, TRACK_NAMES_EMBEDDINGS_PATH
from server.consts.typing_consts import DataClass
from server.logic.playlist_imitation.playlist_imitator_database_creator import PlaylistImitatorDatabaseCreator


def build_prompt(prompt_prefix: str, prompt_suffix: str) -> str:
    return f'{prompt_prefix}\n{prompt_suffix}'


def sample_list(n_candidates: int, n_selected_candidates: int) -> List[int]:
    k = min(n_selected_candidates, n_candidates)
    return random.sample(range(0, n_candidates), k)


def download_database() -> None:
    drive_client = GoogleDriveClient.create()

    if not os.path.exists(DATA_PATH):
        drive_client.download_all_dir_files(
            folder_id=os.environ[DATABASE_FOLDER_DRIVE_ID],
            local_dir=RESOURCES_DIR_PATH
        )

    if not os.path.exists(TRACK_NAMES_EMBEDDINGS_PATH):
        drive_client.download_all_dir_files(
            folder_id=os.environ[TRACK_NAMES_EMBEDDINGS_FOLDER_DRIVE_ID],
            local_dir=RESOURCES_DIR_PATH
        )

    PlaylistImitatorDatabaseCreator().create()


def to_dataclass(serializable: Union[list, dict], dataclass: Type[DataClass]) -> Union[DataClass, List[DataClass]]:
    if isinstance(serializable, dict):
        return dataclass.from_dict(serializable)

    if isinstance(serializable, list):
        return [dataclass.from_dict(elem) for elem in serializable]

    raise ValueError("Cannot serialize values to dataclass that are neither dict or list")
