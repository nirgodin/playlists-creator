import asyncio
from typing import List, Optional
from typing import TypeVar

from flask import Request

from server.consts.api_consts import MAX_SPOTIFY_PLAYLIST_SIZE
from server.consts.app_consts import PLAYLIST_DETAILS, PROMPT
from server.consts.data_consts import URI
from server.consts.openai_consts import QUERY_CONDITIONS_PROMPT_PREFIX_FORMAT, QUERY_CONDITIONS_PROMPT_SUFFIX_FORMAT, \
    TRACKS_AND_ARTISTS_NAMES_PROMPT_FORMAT
from server.controllers.content_controllers.base_content_controller import BaseContentController
from server.data.query_condition import QueryCondition
from server.logic.data_filterer import DataFilterer
from server.logic.openai.columns_details_creator import ColumnsDetailsCreator
from server.logic.openai.openai_adapter import OpenAIAdapter
from server.logic.openai.track_details import TrackDetails
from server.logic.spotify_tracks_collector import SpotifyTracksCollector
from server.utils.general_utils import build_prompt

DataClass = TypeVar('DataClass')


class PromptController(BaseContentController):
    def __init__(self):
        super().__init__()
        self._openai_adapter = OpenAIAdapter()
        self._data_filterer = DataFilterer()
        self._columns_details_creator = ColumnsDetailsCreator()
        self._tracks_collector = SpotifyTracksCollector()

    def _get_request_body(self, client_request: Request) -> dict:
        return client_request.get_json()

    def _generate_tracks_uris(self, request_body: dict) -> Optional[List[str]]:
        user_text = self._extract_prompt_from_request_body(request_body)
        query_conditions_uris = self._generate_uris_from_query_conditions(user_text)

        if query_conditions_uris is not None:
            return query_conditions_uris
        else:
            return self._generate_uris_from_tracks_details(user_text)

    def _generate_playlist_cover_prompt(self, request_body: dict) -> str:
        user_text = self._extract_prompt_from_request_body(request_body)
        return f'{user_text}, digital art'

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

    @staticmethod
    def _extract_prompt_from_request_body(request_body: dict) -> str:
        return request_body[PLAYLIST_DETAILS][PROMPT]
