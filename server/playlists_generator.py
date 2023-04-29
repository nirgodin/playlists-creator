import asyncio
import re
from typing import List, Any, Dict

from dataclasses_json.stringcase import snakecase

from server.data_filterer import DataFilterer
from server.query_condition import QueryCondition

from server.playlists_creator import PlaylistsCreator

URI = 'uri'


class PlaylistsGenerator:
    def __init__(self):
        self._data_filterer = DataFilterer()
        self._playlists_creator = PlaylistsCreator()

    def generate(self, query_conditions: List[QueryCondition], access_code: str, playlist_details: dict) -> None:
        filtered_data = self._data_filterer.filter(query_conditions)
        uris = filtered_data[URI].tolist()
        self._playlists_creator.create(uris, access_code, playlist_details)

    def _pre_process_request_body(self, body: dict) -> List[QueryCondition]:
        pre_processed_body = []
        filter_params = body['filterParams']

        for column_name, column_details in filter_params.items():
            pre_processed_column_name = self._pre_process_column_name(column_name)
            pre_processed_details = {'column': pre_processed_column_name}
            pre_processed_details.update(column_details)
            query_condition = QueryCondition.from_dict(pre_processed_details)

            if query_condition.condition is not None:
                pre_processed_body.append(query_condition)

        return pre_processed_body

    def _pre_process_column_name(self, column_name: str) -> str:
        snakecased_column_name = self._to_snakecase(column_name)
        return re.sub(r'min_|max_', '', snakecased_column_name)

    @staticmethod
    def _to_snakecase(s: str) -> str:
        result = ""

        for i, char in enumerate(s):
            if char.isupper() and i != 0:
                result += "_"
            result += char.lower()

        return result
