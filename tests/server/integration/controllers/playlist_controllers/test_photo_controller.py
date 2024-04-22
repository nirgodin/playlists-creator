import json
from random import randint
from typing import List, Dict, Union
from unittest.mock import MagicMock

from _pytest.fixtures import fixture
from aioresponses import aioresponses
from genie_common.utils import random_alphanumeric_string, random_string_array, random_string_dict
from genie_datastores.postgres.models import PlaylistEndpoint

from server.consts.app_consts import PHOTO
from server.consts.data_consts import TRACKS, URI
from server.controllers.content_controllers.photo_controller import PhotoController
from server.data.case_status import CaseStatus
from server.data.playlist_creation_context import PlaylistCreationContext
from server.logic.ocr.artists_searcher import ArtistsSearcher
from server.logic.ocr.image_text_extractor import ImageTextExtractor
from server.logic.openai.openai_adapter import OpenAIAdapter
from tests.server.integration.controllers.playlist_controllers.base_playlist_controller_test import \
    BasePlaylistControllerTest
from tests.server.integration.controllers.playlist_controllers.playlist_controller_test_context import \
    PlaylistControllerTestContext
from tests.server.utils import random_encoded_image, build_spotify_url, \
    build_chat_completions_response, build_artists_search_response


class TestPhotoController(BasePlaylistControllerTest):
    async def test_post(self, test_context: PlaylistControllerTestContext):
        response = self._request(test_context)
        await self._assert_expected_base_controller_logic(response, test_context)

    @fixture(autouse=True, scope="function")
    def additional_responses(self,
                             artists_ids_to_names: Dict[str, str],
                             uris: List[str],
                             mock_responses: aioresponses) -> None:
        raw_content = list(artists_ids_to_names.values())
        content = json.dumps(raw_content)
        mock_responses.post(
            url='https://api.openai.com/v1/chat/completions',
            payload=build_chat_completions_response(content)
        )

        yield

    @fixture(scope="class")
    def controller(self,
                   context: PlaylistCreationContext,
                   image_text_extractor: ImageTextExtractor,
                   openai_adapter: OpenAIAdapter,
                   artists_searcher: ArtistsSearcher) -> PhotoController:
        return PhotoController(
            context=context,
            image_text_extractor=image_text_extractor,
            openai_adapter=openai_adapter,
            artists_searcher=artists_searcher
        )

    @fixture(scope="class")
    def image_text_extractor(self) -> MagicMock:
        mock_extractor = MagicMock(ImageTextExtractor)
        mock_extractor.extract.return_value = random_alphanumeric_string()

        return mock_extractor

    @fixture(scope="class")
    def endpoint(self) -> PlaylistEndpoint:
        return PlaylistEndpoint.PHOTO

    @fixture(scope="function")
    def payload(self) -> Dict[str, Union[bytes, str, dict]]:
        payload = self._get_basic_request_payload()
        photo = random_encoded_image()
        payload[PHOTO] = f"{random_alphanumeric_string()},{photo}"

        return payload

    @fixture(scope="class")
    def expected_progress_statuses(self) -> List[CaseStatus]:
        return [
            CaseStatus.CREATED,
            CaseStatus.PHOTO,
            CaseStatus.PROMPT,
            CaseStatus.TRACKS,
            CaseStatus.PLAYLIST,
            CaseStatus.COVER,
            CaseStatus.COMPLETED,
        ]

    @fixture(scope="function")
    def uris(self, artists_ids_to_names: Dict[str, str], mock_responses: aioresponses) -> List[str]:
        uris = []

        for artist_id in artists_ids_to_names.keys():
            self._set_single_artist_top_tracks_response(
                artist_id=artist_id,
                uris=uris,
                mock_responses=mock_responses
            )

        yield sorted(uris)

    @fixture(scope="function")
    def artists_ids_to_names(self, mock_responses: aioresponses) -> Dict[str, str]:
        n_artists = randint(1, 5)
        artists = random_string_dict(length=n_artists)

        for artist_id, artist_name in artists.items():
            self._set_single_artist_search_response(
                artist_id=artist_id,
                artist_name=artist_name,
                mock_responses=mock_responses
            )

        yield artists

    @staticmethod
    def _set_single_artist_top_tracks_response(artist_id: str, uris: List[str], mock_responses: aioresponses) -> None:
        url = build_spotify_url(["artists", artist_id, "top-tracks"], params={"market": "US"})
        n_uris = randint(1, 5)
        artist_uris = random_string_array(n_uris)
        payload = {
            TRACKS: [{URI: uri} for uri in artist_uris]
        }
        mock_responses.get(url=url, payload=payload)
        uris.extend(artist_uris)

    @staticmethod
    def _set_single_artist_search_response(artist_id: str, artist_name: str, mock_responses: aioresponses) -> None:
        params = {"q": f"artist:{artist_name}", "type": "artist"}
        url = build_spotify_url(["search"], params)
        payload = build_artists_search_response(artist_id, artist_name)
        mock_responses.get(url=url, payload=payload)
