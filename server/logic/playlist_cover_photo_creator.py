from base64 import b64encode
from tempfile import TemporaryDirectory
from typing import Optional

import requests

from server.consts.api_consts import PLAYLIST_COVER_URL_FORMAT
from server.logic.openai.dalle_adapter import DallEAdapter
from server.utils.image_utils import save_image_as_jpeg


class PlaylistCoverPhotoCreator:
    def __init__(self):
        self._dalle_adapter = DallEAdapter()

    def put_playlist_cover(self, headers: dict, playlist_id: str, image_path: Optional[str]) -> None:
        if image_path is None:
            return

        url = PLAYLIST_COVER_URL_FORMAT.format(playlist_id)
        image = self._encode_image_to_base64(image_path)
        requests.put(
            url=url,
            data=image,
            headers=headers
        )

    def _create_image(self, prompt: str) -> Optional[str]:
        with TemporaryDirectory() as dir_name:
            image_path = self._dalle_adapter.create_image(prompt, dir_path=dir_name)

            if image_path is not None:
                return self._encode_image_to_base64(image_path)

    @staticmethod
    def _encode_image_to_base64(image_path: str) -> str:
        formatted_image_path = save_image_as_jpeg(image_path)

        with open(formatted_image_path, "rb") as image_file:
            encoded_image = b64encode(image_file.read())

        return encoded_image.decode("utf-8")
