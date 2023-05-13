import asyncio
import json
import os.path
from tempfile import TemporaryDirectory
from typing import List

from flask import Response, request

from server.controllers.base_content_controller import BaseContentController
from server.logic.ocr.image_playlist_creator import ImagePlaylistCreator
from server.utils import sample_list


class PhotoController(BaseContentController):
    def __init__(self, max_playlist_size: int = 100):
        super().__init__()
        self._image_playlist_creator = ImagePlaylistCreator()
        self._max_playlist_size = max_playlist_size

    def post(self) -> Response:
        body = json.loads(request.files['data'].read())
        file = request.files['image']
        uris = self._get_tracks_uris(file)

        return self._generate_response(body, [], uris)

    def _get_tracks_uris(self, file) -> List[str]:
        with TemporaryDirectory() as tmpdirname:
            path = os.path.join(tmpdirname, file.name)
            file.save(path)
            uris = asyncio.run(self._image_playlist_creator.create_playlist(path))

        n_candidates = len(uris)
        n_selected_candidates = min(n_candidates, self._max_playlist_size)
        selected_uris_indexes = sample_list(n_candidates, n_selected_candidates)

        return [uris[i] for i in selected_uris_indexes]
