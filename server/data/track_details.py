from dataclasses import dataclass

from dataclasses_json import dataclass_json
from spotipyio import SearchItemMetadata, SearchItemFilters
from spotipyio.logic.collectors.search_collectors.search_item import SearchItem
from spotipyio.logic.collectors.search_collectors.spotify_search_type import SpotifySearchType


@dataclass_json
@dataclass
class TrackDetails:
    track_name: str
    artist_name: str

    def to_search_item(self) -> SearchItem:
        return SearchItem(
            filters=SearchItemFilters(
                track=self.track_name,
                artist=self.artist_name
            ),
            metadata=SearchItemMetadata(
                search_types=[SpotifySearchType.TRACK],
            )
        )
