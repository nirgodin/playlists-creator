import os.path
import random
from functools import reduce
from typing import List, Dict, Optional

from server.consts.api_consts import ACCESS_TOKEN
from server.consts.env_consts import DATABASE_FOLDER_DRIVE_ID
from server.consts.path_consts import RESOURCES_DIR_PATH, DATA_PATH
from server.data.spotify_grant_type import SpotifyGrantType
from server.logic.access_token_generator import AccessTokenGenerator
from server.logic.configuration_photo_prompt.z_scores_metadata_creator import ZScoresMetadataCreator
from server.logic.playlist_imitation.playlist_imitator_database_creator import PlaylistImitatorDatabaseCreator
from server.tools.google_drive.google_drive_adapter import GoogleDriveAdapter


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
    if os.path.exists(DATA_PATH):
        return

    GoogleDriveAdapter().download_all_dir_files(
        folder_id=os.environ[DATABASE_FOLDER_DRIVE_ID],
        local_dir=RESOURCES_DIR_PATH
    )
    ZScoresMetadataCreator().create()
    PlaylistImitatorDatabaseCreator().create()


def chain_dicts(dicts: List[dict]) -> dict:
    return reduce(lambda dict1, dict2: {**dict1, **dict2}, dicts)
