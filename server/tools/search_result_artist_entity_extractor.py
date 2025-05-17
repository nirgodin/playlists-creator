from typing import List

from genie_common.utils import safe_nested_get
from spotipyio.tools.extractors import IEntityExtractor

from server.consts.data_consts import ITEMS, ARTISTS, NAME


class SearchResultArtistEntityExtractor(IEntityExtractor):
    def extract(self, entity: dict) -> List[str]:
        artists = []
        items = safe_nested_get(entity, [ARTISTS, ITEMS], default=[])

        if items:
            first_item = items[0]
            artists.append(first_item[NAME])

        return artists

    @property
    def name(self) -> str:
        return "artist"
