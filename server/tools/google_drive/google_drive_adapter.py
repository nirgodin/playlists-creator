import json
import os

from server.consts.env_consts import GOOGLE_SERVICE_ACCOUNT_CREDENTIALS
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from server.tools.logging import logger


class GoogleDriveAdapter:
    def download_all_dir_files(self, folder_id: str, local_dir: str) -> None:
        logger.info(
            msg="Starting to download all directory files from Google Drive",
            extra={"folder_id": folder_id, "local_dir": local_dir}
        )
        query = f"'{folder_id}' in parents"
        results = self._drive_service.files().list(q=query).execute()
        files = results.get('files', [])

        for file in files:
            file_path = os.path.join(local_dir, file['name'])
            self.download(file_id=file['id'], local_path=file_path)

    def download(self, file_id: str, local_path: str) -> None:
        extra = {"file_id": file_id, "local_path": local_path}
        logger.info("Starting to download file from Google Drive", extra=extra)
        file_content = self._drive_service.files().get_media(fileId=file_id).execute()

        with open(local_path, 'wb') as f:
            f.write(file_content)

        logger.info(f'Successfully downloaded file from Google Drive', extra=extra)

    @property
    def _drive_service(self):
        credentials = json.loads(os.environ[GOOGLE_SERVICE_ACCOUNT_CREDENTIALS])

        return build(
            serviceName='drive',
            version='v3',
            credentials=Credentials.from_service_account_info(credentials)
        )
