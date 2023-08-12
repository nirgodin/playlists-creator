from typing import Optional, List

from aiohttp import ClientSession

from server.consts.api_consts import ID
from server.consts.prompt_consts import PHOTO_ARTISTS_PROMPT_PREFIX
from server.logic.ocr.artists_collector import ArtistsCollector
from server.logic.ocr.artists_filterer import ArtistsFilterer
from server.logic.ocr.artists_top_tracks_collector import ArtistsTopTracksCollector
from server.logic.ocr.image_text_extractor import ImageTextExtractor
from server.logic.openai.openai_adapter import OpenAIAdapter
from server.logic.openai.openai_client import OpenAIClient
from server.utils.general_utils import build_prompt


class TracksURIsImageExtractor:
    def __init__(self, session: ClientSession):
        self._image_text_extractor = ImageTextExtractor()
        self._openai_adapter = OpenAIAdapter(OpenAIClient(session))
        self._artists_collector = ArtistsCollector(session)
        self._artists_filterer = ArtistsFilterer()
        self._top_tracks_collector = ArtistsTopTracksCollector(session)

    async def extract_tracks_uris(self, image_path: str, language: str = 'eng', country: str = 'US') -> Optional[List[str]]:
        artists_names = await self._extract_artists_names(image_path, language)
        if not artists_names:
            return

        artists_details = await self._artists_collector.collect(artists_names)
        relevant_artists = self._artists_filterer.filter_relevant_artists(artists_details)
        artists_ids = [artist[ID] for artist in relevant_artists]
        top_tracks = await self._top_tracks_collector.collect(artists_ids, country)

        return self._extract_tracks_uris(top_tracks)

    async def _extract_artists_names(self, image_path: str, language: str = 'eng') -> Optional[List[str]]:
        image_text = self._image_text_extractor.extract_text(image_path, language)
        prompt_suffix = f'```\n{image_text}```'
        prompt = build_prompt(PHOTO_ARTISTS_PROMPT_PREFIX, prompt_suffix)

        return await self._openai_adapter.chat_completions(prompt)

    @staticmethod
    def _extract_tracks_uris(tracks: List[List[dict]]) -> List[str]:
        uris = []

        for artist_tracks in tracks:
            for track in artist_tracks:
                uris.append(track['uri'])

        return uris
