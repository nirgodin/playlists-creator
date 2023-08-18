from base64 import b64encode
from typing import Optional

from aiohttp import ClientSession

from server.consts.api_consts import PLAYLIST_COVER_URL_FORMAT
from server.utils.image_utils import save_image_as_jpeg


class PlaylistCoverPhotoCreator:
    def __init__(self, session: ClientSession):
        self._session = session

    async def put_playlist_cover(self, headers: dict, playlist_id: str, image_path: Optional[str]) -> None:
        if image_path is None:
            return

        url = PLAYLIST_COVER_URL_FORMAT.format(playlist_id)
        image = self._encode_image_to_base64(image_path)

        async with self._session.put(url=url, data=image, headers=headers) as raw_response:
            raw_response.raise_for_status()  # TODO: Handle cases where 413 status: response entity is too large

    @staticmethod
    def _encode_image_to_base64(image_path: str) -> str:
        formatted_image_path = save_image_as_jpeg(image_path)

        with open(formatted_image_path, "rb") as image_file:
            encoded_image = b64encode(image_file.read())

        return encoded_image.decode("utf-8")
