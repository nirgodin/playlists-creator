import os
import urllib

import openai

from server.consts.env_consts import OPENAI_API_KEY


class DallEAdapter:
    def __init__(self):
        openai.api_key = os.environ[OPENAI_API_KEY]
        self._openai_model = openai.ChatCompletion()

    def create_image(self, prompt: str, dir_path: str) -> str:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512",
        )
        image_url = response['data'][0]['url']
        image_creation_timestamp = response['created']
        file_name = f'{image_creation_timestamp}.png'
        image_path = os.path.join(dir_path, file_name)
        urllib.request.urlretrieve(image_url, image_path)

        return image_path


if __name__ == '__main__':
    DallEAdapter().create_image('Hip hop songs with high energy and danceability, digital art', dir_path='/Users/nirgodin/Downloads')
