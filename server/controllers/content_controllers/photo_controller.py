import json
from typing import Optional

from aiohttp import ClientSession
from flask import Request
from werkzeug.datastructures import FileStorage

from server.consts.api_consts import MAX_SPOTIFY_PLAYLIST_SIZE
from server.consts.app_consts import REQUEST_BODY, PHOTO
from server.controllers.content_controllers.base_content_controller import BaseContentController
from server.data.playlist_resources import PlaylistResources
from server.logic.ocr.tracks_uris_image_extractor import TracksURIsImageExtractor
from server.utils.general_utils import sample_list
from server.utils.image_utils import current_timestamp_image_path


class PhotoController(BaseContentController):
    def __init__(self, session: ClientSession):
        super().__init__(session)
        self._tracks_uris_extractor = TracksURIsImageExtractor(session)

    def _get_request_body(self, client_request: Request) -> dict:
        body = client_request.files[REQUEST_BODY]
        data = body.read()
        request_body = json.loads(data)
        request_body[PHOTO] = client_request.files[PHOTO]

        return request_body

    async def _generate_playlist_resources(self, request_body: dict, dir_path: str) -> PlaylistResources:
        cover_image_path = self._save_photo(request_body[PHOTO], dir_path)
        uris = await self._tracks_uris_extractor.extract_tracks_uris(cover_image_path)

        if uris is None:
            return PlaylistResources(None, None)

        n_candidates = len(uris)
        selected_uris_indexes = sample_list(n_candidates, MAX_SPOTIFY_PLAYLIST_SIZE)
        tracks_uris = [uris[i] for i in selected_uris_indexes]

        return PlaylistResources(
            uris=tracks_uris,
            cover_image_path=cover_image_path
        )

    @staticmethod
    def _save_photo(photo: FileStorage, dir_path: str) -> str:
        image_path = current_timestamp_image_path(dir_path)
        photo.save(image_path)

        return image_path

    def _generate_playlist_cover(self, request_body: dict, image_path: str) -> Optional[str]:
        return image_path
