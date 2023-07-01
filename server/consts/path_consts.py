import os.path
from pathlib import Path


def _get_resources_dir_path() -> str:
    current_dir_path = Path(os.path.dirname(__file__))
    server_dir_path = current_dir_path.parent

    return os.path.join(server_dir_path, 'resources')


RESOURCES_DIR_PATH = _get_resources_dir_path()
DATA_PATH = f'{RESOURCES_DIR_PATH}/playlists_creator_database.csv'
COLUMNS_DESCRIPTIONS_PATH = f'{RESOURCES_DIR_PATH}/columns_details_descriptions.json'
COLUMNS_Z_SCORES_METADATA_PATH = f'{RESOURCES_DIR_PATH}/z_scores_metadata.json'
PLAYLIST_IMITATOR_DATABASE_PATH = f'{RESOURCES_DIR_PATH}/playlist_imitator_database.csv'
PLAYLIST_IMITATOR_PIPELINE_PATH = f'{RESOURCES_DIR_PATH}/pipeline.pkl'
