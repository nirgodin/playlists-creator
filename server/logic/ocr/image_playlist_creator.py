import asyncio
import json
from typing import Optional, List

from server.logic.ocr.artists_collector import ArtistsCollector
from server.logic.ocr.artists_filterer import ArtistsFilterer
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


class ImagePlaylistCreator:
    def __init__(self):
        self._image_text_extractor = ImageTextExtractor()
        self._openai_adapter = OpenAIAdapter()
        self._artists_collector = ArtistsCollector()
        self._artists_filterer = ArtistsFilterer()

    async def create_playlist(self, image_path: str, language: str = 'eng') -> Optional[str]:
        # artists_names = self._get_artists_names(image_path, language)
        # if not artists_names:
        #     return
        #
        # artists_details = await self._artists_collector.collect(artists_names)
        with open('/Users/nirgodin/Downloads/artists.json', 'r') as f:
            artists_details = json.load(f)

        relevant_artists = self._artists_filterer.filter_relevant_artists(artists_details)
        print('b')

    def _get_artists_names(self, image_path: str, language: str = 'eng') -> Optional[List[str]]:
        image_text = self._image_text_extractor.extract_text(image_path, language)
        prompt_suffix = f'```\n{image_text}```'
        prompt = build_prompt(PROMPT_PREFIX, prompt_suffix)

        return self._openai_adapter.fetch_openai(prompt)


if __name__ == '__main__':
    IMAGE_PATH = '/Users/nirgodin/Downloads/coa_2023_4x5_v2.jpg'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ImagePlaylistCreator().create_playlist(IMAGE_PATH))
