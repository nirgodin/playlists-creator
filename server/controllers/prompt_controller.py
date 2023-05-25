import asyncio
from typing import List, Optional, TypeVar

from flask import Response, request

from server.consts.api_consts import MAX_SPOTIFY_PLAYLIST_SIZE
from server.consts.app_consts import PLAYLIST_DETAILS, PROMPT, ACCESS_CODE
from server.consts.data_consts import URI
from server.consts.openai_consts import QUERY_CONDITIONS_PROMPT_PREFIX_FORMAT, QUERY_CONDITIONS_PROMPT_SUFFIX_FORMAT, \
    TRACKS_AND_ARTISTS_NAMES_PROMPT_FORMAT
from server.controllers.base_content_controller import BaseContentController
from server.data.query_condition import QueryCondition
from server.data.spotify_grant_type import SpotifyGrantType
from server.logic.access_token_generator import AccessTokenGenerator
from server.logic.openai.columns_details_creator import ColumnsDetailsCreator
from server.logic.openai.openai_adapter import OpenAIAdapter
from server.logic.openai.track_details import TrackDetails
from server.logic.playlist_cover_photo_creator import PlaylistCoverPhotoCreator
from server.logic.spotify_tracks_collector import SpotifyTracksCollector
from server.utils import build_prompt

DataClass = TypeVar('DataClass')


class PromptController(BaseContentController):
    def __init__(self):
        super().__init__()
        self._openai_adapter = OpenAIAdapter()
        self._columns_details_creator = ColumnsDetailsCreator()
        self._tracks_collector = SpotifyTracksCollector()

    def post(self) -> Response:
        body = request.get_json()
        user_text = body[PLAYLIST_DETAILS][PROMPT]
        query_conditions_uris = self._generate_uris_from_query_conditions(user_text)

        if query_conditions_uris is not None:
            return self._generate_response(body, query_conditions_uris)
        else:
            track_details_uris = self._generate_uris_from_tracks_details(user_text)
            return self._generate_response(body, track_details_uris)
        # response = AccessTokenGenerator.generate(grant_type=SpotifyGrantType.AUTHORIZATION_CODE, access_code=body[ACCESS_CODE])
        # headers = self._build_request_headers(response)
        # PlaylistCoverPhotoCreator().put_playlist_cover(headers=headers, playlist_id='0tp13KbV1k1qoGzgfTpa36', prompt=body[PLAYLIST_DETAILS][PROMPT])

    def _generate_uris_from_query_conditions(self, user_text: str) -> Optional[List[str]]:
        prompt = self._build_query_conditions_prompt(user_text)
        json_serialized_response = self._openai_adapter.fetch_openai(prompt, retries_left=1)
        query_conditions = self._serialize_openai_response(json_serialized_response, klazz=QueryCondition)

        if query_conditions is not None:
            return self._data_filterer.filter(query_conditions)

    def _build_query_conditions_prompt(self, user_text: str) -> str:
        columns_details = self._columns_details_creator.create()
        prompt_prefix = QUERY_CONDITIONS_PROMPT_PREFIX_FORMAT.format(columns_details=columns_details)
        prompt_suffix = QUERY_CONDITIONS_PROMPT_SUFFIX_FORMAT.format(user_text=user_text)

        return build_prompt(prompt_prefix, prompt_suffix)

    @staticmethod
    def _serialize_openai_response(json_serialized_response: Optional[List[dict]], klazz: DataClass) -> Optional[list]:
        if json_serialized_response is None:
            return

        try:
            return [klazz.from_dict(condition) for condition in json_serialized_response]
        except:
            return

    def _generate_uris_from_tracks_details(self, user_text: str) -> Optional[List[str]]:
        prompt = TRACKS_AND_ARTISTS_NAMES_PROMPT_FORMAT.format(user_text=user_text)
        json_serialized_response = self._openai_adapter.fetch_openai(prompt, retries_left=2)
        tracks_details = self._serialize_openai_response(json_serialized_response, klazz=TrackDetails)

        if tracks_details is None:
            return

        tracks = asyncio.run(self._tracks_collector.collect(tracks_details))
        return [track[URI] for track in tracks][:MAX_SPOTIFY_PLAYLIST_SIZE]

    def _build_uris_prompt(self, user_text: str) -> str:
        columns_details = self._columns_details_creator.create()
        prompt_prefix = QUERY_CONDITIONS_PROMPT_PREFIX_FORMAT.format(columns_details=columns_details)
        prompt_suffix = QUERY_CONDITIONS_PROMPT_SUFFIX_FORMAT.format(user_text=user_text)

        return build_prompt(prompt_prefix, prompt_suffix)
