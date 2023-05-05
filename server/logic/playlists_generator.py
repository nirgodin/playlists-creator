import re
from typing import List

from server.consts.app_consts import FILTER_PARAMS
from server.consts.data_consts import URI
from server.logic.data_filterer import DataFilterer
from server.logic.playlists_creator import PlaylistsCreator
from server.data.query_condition import QueryCondition


class PlaylistsGenerator:
    def __init__(self):
        self._data_filterer = DataFilterer()
        self._playlists_creator = PlaylistsCreator()

    def generate(self, query_conditions: List[QueryCondition], access_code: str, playlist_details: dict) -> str:
        filtered_data = self._data_filterer.filter(query_conditions)
        uris = filtered_data[URI].tolist()
        playlist_link = self._playlists_creator.create(uris, access_code, playlist_details)

        return playlist_link

    def _pre_process_request_body(self, body: dict) -> List[QueryCondition]:
        pre_processed_body = []
        filter_params = body[FILTER_PARAMS]

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
