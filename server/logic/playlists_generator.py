from typing import List

from server.consts.data_consts import URI
from server.data.query_condition import QueryCondition
from server.logic.data_filterer import DataFilterer
from server.logic.playlists_creator import PlaylistsCreator


class PlaylistsGenerator:
    def __init__(self):
        self._data_filterer = DataFilterer()
        self._playlists_creator = PlaylistsCreator()

    def generate(self, query_conditions: List[QueryCondition], access_code: str, playlist_details: dict) -> str:
        filtered_data = self._data_filterer.filter(query_conditions)
        uris = filtered_data[URI].tolist()
        playlist_link = self._playlists_creator.create(uris, access_code, playlist_details)

        return playlist_link
