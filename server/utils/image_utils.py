import io
import os

from PIL import Image
from aiohttp import ClientSession
from genie_common.tools import logger
from genie_common.utils import fetch_image

from server.consts.image_consts import JPG_FILE_SUFFIX, RGB
from server.utils.datetime_utils import get_current_timestamp


async def save_image_from_url(session: ClientSession, image_url: str, output_path: str) -> None:
    logger.info(f"Fetching image from `{image_url}`")
    image_bytes = await fetch_image(session, image_url)
    save_image_from_bytes(image_bytes, output_path)
    logger.info(f"Successfully fetched image and saved it on `{output_path}`")


def save_image_from_bytes(image: bytes, output_path: str) -> None:
    file = io.BytesIO(image)
    image = Image.open(file)
    image.save(output_path)


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
