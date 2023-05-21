from base64 import b64encode

import requests

from server.consts.api_consts import PLAYLIST_COVER_URL_FORMAT


class PlaylistCoverPhotoCreator:
    def put_playlist_cover(self, headers: dict, playlist_id: str, image_path: str) -> None:
        url = PLAYLIST_COVER_URL_FORMAT.format(playlist_id)
        image = self._encode_image_to_base64(image_path)
        res = requests.put(
            url=url,
            data=image,
            headers=headers
        )
        print('b')

    @staticmethod
    def _encode_image_to_base64(image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            encoded_image = b64encode(image_file.read())

        return encoded_image.decode("utf-8")
