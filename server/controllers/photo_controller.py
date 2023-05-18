import asyncio
import json
import os.path
from tempfile import TemporaryDirectory
from typing import List, Optional

from flask import Response, request
from werkzeug.datastructures import FileStorage

from server.consts.app_consts import REQUEST_BODY, PHOTO
from server.controllers.base_content_controller import BaseContentController
from server.logic.ocr.tracks_uris_image_extractor import TracksURIsImageExtractor
from server.utils import sample_list


class PhotoController(BaseContentController):
    def __init__(self, max_playlist_size: int = 100):
        super().__init__()
        self._tracks_uris_extractor = TracksURIsImageExtractor()
        self._max_playlist_size = max_playlist_size

    def post(self) -> Response:
        body = self._get_body()
        photo = request.files[PHOTO]
        uris = self._get_tracks_uris(photo)

        return self._generate_response(body, uris)

    @staticmethod
    def _get_body() -> dict:
        body = request.files[REQUEST_BODY]
        data = body.read()

        return json.loads(data)

    def _get_tracks_uris(self, photo: FileStorage) -> List[str]:
        uris = self._get_tracks_uri_from_photo(photo)
        n_candidates = len(uris)
        n_selected_candidates = min(n_candidates, self._max_playlist_size)
        selected_uris_indexes = sample_list(n_candidates, n_selected_candidates)

        return [uris[i] for i in selected_uris_indexes]

    def _get_tracks_uri_from_photo(self, photo: FileStorage) -> Optional[List[str]]:
        with TemporaryDirectory() as dir_name:
            path = os.path.join(dir_name, photo.name)
            photo.save(path)

            return asyncio.run(self._tracks_uris_extractor.extract_tracks_uris(path))
