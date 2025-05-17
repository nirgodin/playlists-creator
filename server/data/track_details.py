from dataclasses import dataclass

from dataclasses_json import dataclass_json
from spotipyio.models import SearchItemMetadata, SearchItemFilters, SearchItem, SpotifySearchType


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
