import asyncio
import json
import os.path
from tempfile import TemporaryDirectory
from typing import List, Optional

from flask import Request
from werkzeug.datastructures import FileStorage

from server.consts.api_consts import MAX_SPOTIFY_PLAYLIST_SIZE
from server.consts.app_consts import REQUEST_BODY, PHOTO
from server.controllers.content_controllers.base_content_controller import BaseContentController
from server.logic.ocr.tracks_uris_image_extractor import TracksURIsImageExtractor
from server.utils.general_utils import sample_list


class PhotoController(BaseContentController):
    def __init__(self):
        super().__init__()
        self._tracks_uris_extractor = TracksURIsImageExtractor()

    def _get_request_body(self, client_request: Request) -> dict:
        body = client_request.files[REQUEST_BODY]
        data = body.read()
        request_body = json.loads(data)
        request_body[PHOTO] = client_request.files[PHOTO]

        return request_body

    def _generate_tracks_uris(self, request_body: dict) -> Optional[List[str]]:
        uris = self._get_tracks_uri_from_photo(request_body[PHOTO])
        if uris is None:
            return

        n_candidates = len(uris)
        n_selected_candidates = min(n_candidates, MAX_SPOTIFY_PLAYLIST_SIZE)
        selected_uris_indexes = sample_list(n_candidates, n_selected_candidates)

        return [uris[i] for i in selected_uris_indexes]

    def _get_tracks_uri_from_photo(self, photo: FileStorage) -> Optional[List[str]]:
        with TemporaryDirectory() as dir_name:
            path = os.path.join(dir_name, photo.name)
            photo.save(path)

            return asyncio.run(self._tracks_uris_extractor.extract_tracks_uris(path))

    def _generate_playlist_cover_prompt(self, request_body: dict) -> str:
        raise   # TODO: Fix to enable cover
