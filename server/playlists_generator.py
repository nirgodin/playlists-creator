import asyncio
import re
from typing import List, Any, Dict

from server.data_filterer import DataFilterer
from server.query_condition import QueryCondition

from server.playlists_creator import PlaylistsCreator

URI = 'uri'


class PlaylistsGenerator:
    def __init__(self):
        self._data_filterer = DataFilterer()
        self._playlists_creator = PlaylistsCreator()

    def generate(self, body: dict) -> None:
        query_conditions = self._pre_process_request_body(body)
        filtered_data = self._data_filterer.filter(query_conditions)
        uris = filtered_data[URI].tolist()
        access_code = body['accessCode']
        playlist_details = body['playlistDetails']
        self._playlists_creator.create(uris, access_code, playlist_details)

    @staticmethod
    def _pre_process_request_body(body: dict) -> List[QueryCondition]:
        pre_processed_body = []
        filter_params = body['filterParams']

        for column_name, column_details in filter_params.items():
            pre_processed_column_name = re.sub(r'min|max', '', column_name).lower()
            pre_processed_details = {'column': pre_processed_column_name}
            pre_processed_details.update(column_details)
            query_condition = QueryCondition.from_dict(pre_processed_details)

            if query_condition.condition is not None:
                pre_processed_body.append(query_condition)

        return pre_processed_body
