import os

import requests
import io
from PIL import Image

from server.consts.image_consts import JPG_FILE_SUFFIX, RGB
from server.utils.datetime_utils import get_current_timestamp


def save_image_from_url(image_url: str, output_path: str) -> None:
    response = requests.get(image_url)

    if response.status_code != 200:
        print("Failed to download the image.")
        return

    image_bytes = response.content
    file = io.BytesIO(image_bytes)
    image = Image.open(file)
    image.save(output_path)
    print("Successfully saved image")


def save_image_as_jpeg(image_path: str) -> str:
    image = Image.open(image_path)
    rgb_image = image.convert(RGB)
    original_file_extension = os.path.splitext(image_path)[-1]
    formatted_image_path = image_path.replace(original_file_extension, JPG_FILE_SUFFIX)
    rgb_image.save(formatted_image_path)

    return formatted_image_path


def current_timestamp_image_path(dir_path: str) -> str:
    timestamp = get_current_timestamp()
    file_name = f'{timestamp}.png'

    return os.path.join(dir_path, file_name)
