import asyncio
import json
from typing import Optional, List

from server.consts.api_consts import ID
from server.logic.ocr.artists_collector import ArtistsCollector
from server.logic.ocr.artists_filterer import ArtistsFilterer
from server.logic.ocr.artists_top_tracks_collector import ArtistsTopTracksCollector
from server.logic.ocr.image_text_extractor import ImageTextExtractor
from server.logic.openai.openai_adapter import OpenAIAdapter
from server.utils import build_prompt

PROMPT_PREFIX = """\
Please extract from the following text, denoted in triple brackets, all music artists names you can find. You should \
return the names in a JSON serializable array, where each entry contains a single artist name. Your response should 
include the JSON array and ONLY it. It should be serializable by a single Python `json.loads` command. For example, \
given the following text:
```
EMINEM: tric Bry ili bopgameempiiges Kid cudi LAROI-Charfi Ruj-dmc, ~
```
Your response should look like this:
```
[
    eminem,
    kid cudi,
    run dmc
]
```
 
In case you do not detect any artists name in the text, return an empty array.
The text is:
"""


class TracksURIsImageExtractor:
    def __init__(self):
        self._image_text_extractor = ImageTextExtractor()
        self._openai_adapter = OpenAIAdapter()
        self._artists_collector = ArtistsCollector()
        self._artists_filterer = ArtistsFilterer()
        self._top_tracks_collector = ArtistsTopTracksCollector()

    async def extract_tracks_uris(self, image_path: str, language: str = 'eng', country: str = 'US') -> Optional[List[str]]:
        artists_names = self._extract_artists_names(image_path, language)
        if not artists_names:
            return

        artists_details = await self._artists_collector.collect(artists_names)
        relevant_artists = self._artists_filterer.filter_relevant_artists(artists_details)
        artists_ids = [artist[ID] for artist in relevant_artists]
        top_tracks = await self._top_tracks_collector.collect(artists_ids, country)

        return self._extract_tracks_uris(top_tracks)

    def _extract_artists_names(self, image_path: str, language: str = 'eng') -> Optional[List[str]]:
        image_text = self._image_text_extractor.extract_text(image_path, language)
        prompt_suffix = f'```\n{image_text}```'
        prompt = build_prompt(PROMPT_PREFIX, prompt_suffix)

        return self._openai_adapter.fetch_openai(prompt)

    @staticmethod
    def _extract_tracks_uris(tracks: List[List[dict]]) -> List[str]:
        uris = []

        for artist_tracks in tracks:
            for track in artist_tracks:
                uris.append(track['uri'])

        return uris


if __name__ == '__main__':
    IMAGE_PATH = '/Users/nirgodin/Downloads/coa_2023_4x5_v2.jpg'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(TracksURIsImageExtractor().extract_tracks_uris(IMAGE_PATH))
