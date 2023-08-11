import os
import urllib
from typing import Optional

import openai

from server.consts.data_consts import DATA, URL, CREATED
from server.consts.env_consts import OPENAI_API_KEY
from server.utils.image_utils import save_image_from_url


class DallEAdapter:
    def __init__(self):
        openai.api_key = os.environ[OPENAI_API_KEY]
        self._openai_model = openai.ChatCompletion()

    def create_image(self, prompt: str, image_path: str) -> Optional[str]:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512",
        )
        return self._save_result(response, image_path)

    def variate_image(self, original_image_path: str, image_path: str) -> Optional[str]:
        response = openai.Image.create_variation(
            image=open(original_image_path, 'rb'),
            n=1,
            size="512x512",
        )
        return self._save_result(response, image_path)

    @staticmethod
    def _save_result(response: dict, image_path: str) -> Optional[str]:
        image_url = response[DATA][0][URL]
        image_creation_timestamp = response[CREATED]
        file_name = f'{image_creation_timestamp}.png'
        original_image_dir_path = os.path.dirname(image_path)
        created_image_path = os.path.join(original_image_dir_path, file_name)
        save_image_from_url(image_url, created_image_path)

        if os.path.exists(image_path):
            return created_image_path
