import asyncio
from typing import List

from server.data_filterer import DataFilterer
from server.query_condition import QueryCondition

from server.playlists_creator import PlaylistsCreator

URI = 'uri'


class PlaylistsGenerator:
    def __init__(self):
        self._data_filterer = DataFilterer()
        self._playlists_creator = PlaylistsCreator()

    def generate(self, query_conditions: List[QueryCondition], user_id: str, public: bool = True) -> None:
        filtered_data = self._data_filterer.filter(query_conditions)
        uris = filtered_data[URI].tolist()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._playlists_creator.create(uris=uris, user_id=user_id, public=public))
