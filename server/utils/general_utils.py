import os.path
import random
from functools import reduce
from typing import List, Dict, Optional, Union, Type

from genie_common.google import GoogleDriveAdapter

from server.consts.api_consts import ACCESS_TOKEN
from server.consts.env_consts import DATABASE_FOLDER_DRIVE_ID, TRACK_NAMES_EMBEDDINGS_FOLDER_DRIVE_ID
from server.consts.path_consts import RESOURCES_DIR_PATH, DATA_PATH, TRACK_NAMES_EMBEDDINGS_PATH
from server.consts.typing_consts import DataClass
from server.data.spotify_grant_type import SpotifyGrantType
from server.logic.access_token_generator import AccessTokenGenerator
from server.logic.configuration_photo_prompt.z_scores_metadata_creator import ZScoresMetadataCreator
from server.logic.playlist_imitation.playlist_imitator_database_creator import PlaylistImitatorDatabaseCreator


def build_prompt(prompt_prefix: str, prompt_suffix: str) -> str:
    return f'{prompt_prefix}\n{prompt_suffix}'


async def build_spotify_client_credentials_headers(access_token_generator: AccessTokenGenerator) -> Dict[str, str]:
    response = await access_token_generator.generate(SpotifyGrantType.CLIENT_CREDENTIALS)
    access_token = response[ACCESS_TOKEN]

    return build_spotify_headers(access_token)


def build_spotify_headers(access_token: str) -> Optional[Dict[str, str]]:
    if access_token is not None:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }


def sample_list(n_candidates: int, n_selected_candidates: int) -> List[int]:
    k = min(n_selected_candidates, n_candidates)
    return random.sample(range(0, n_candidates), k)


def string_to_boolean(s: str) -> bool:
    return s.lower() == 'true'


def download_database() -> None:
    drive_adapter = GoogleDriveAdapter.create()

    if not os.path.exists(DATA_PATH):
        drive_adapter.download_all_dir_files(
            folder_id=os.environ[DATABASE_FOLDER_DRIVE_ID],
            local_dir=RESOURCES_DIR_PATH
        )

    if not os.path.exists(TRACK_NAMES_EMBEDDINGS_PATH):
        drive_adapter.download_all_dir_files(
            folder_id=os.environ[TRACK_NAMES_EMBEDDINGS_FOLDER_DRIVE_ID],
            local_dir=RESOURCES_DIR_PATH
        )

    ZScoresMetadataCreator().create()
    PlaylistImitatorDatabaseCreator().create()


def chain_dicts(dicts: List[dict]) -> dict:
    return reduce(lambda dict1, dict2: {**dict1, **dict2}, dicts)


def to_dataclass(serializable: Union[list, dict], dataclass: Type[DataClass]) -> Union[DataClass, List[DataClass]]:
    if isinstance(serializable, dict):
        return dataclass.from_dict(serializable)

    if isinstance(serializable, list):
        return [dataclass.from_dict(elem) for elem in serializable]

    raise ValueError("Cannot serialize values to dataclass that are neither dict or list")
