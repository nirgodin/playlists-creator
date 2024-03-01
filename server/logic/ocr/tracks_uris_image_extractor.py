from typing import Optional, List, Dict

from genie_common.tools import logger
from spotipyio import SpotifyClient

from server.consts.api_consts import ID
from server.consts.data_consts import URI, TRACKS
from server.consts.prompt_consts import PHOTO_ARTISTS_PROMPT_PREFIX
from server.data.chat_completions_request import ChatCompletionsRequest
from server.logic.ocr.artists_collector import ArtistsCollector
from server.logic.ocr.artists_filterer import ArtistsFilterer
from server.logic.ocr.image_text_extractor import ImageTextExtractor
from server.logic.openai.openai_adapter import OpenAIAdapter
from server.tools.case_progress_reporter import CaseProgressReporter
from server.utils.general_utils import build_prompt


class TracksURIsImageExtractor:
    def __init__(self,
                 openai_adapter: OpenAIAdapter,
                 artists_collector: ArtistsCollector,
                 image_text_extractor: ImageTextExtractor,
                 case_progress_reporter: CaseProgressReporter,
                 artists_filterer: ArtistsFilterer = ArtistsFilterer()):
        self._openai_adapter = openai_adapter
        self._image_text_extractor = image_text_extractor
        self._artists_collector = artists_collector
        self._case_progress_reporter = case_progress_reporter
        self._artists_filterer = artists_filterer

    async def extract_tracks_uris(self,
                                  case_id: str,
                                  image_path: str,
                                  spotify_client: SpotifyClient,
                                  language: str = 'eng',
                                  country: str = 'US') -> Optional[List[str]]:
        artists_names = await self._extract_artists_names(case_id, image_path, language)
        if not artists_names:
            return

        async with self._case_progress_reporter.report(case_id=case_id, status="tracks"):
            return await self._generate_tracks_uris(
                artists_names=artists_names,
                spotify_client=spotify_client,
                country=country
            )

    async def _extract_artists_names(self, case_id: str, image_path: str, language: str) -> Optional[List[str]]:
        logger.info("Extracting artists names from provided photo")
        image_text = await self._image_text_extractor.extract_text(
            case_id=case_id,
            image_path=image_path,
            language=language
        )
        prompt_suffix = f'```\n{image_text}```'
        prompt = build_prompt(PHOTO_ARTISTS_PROMPT_PREFIX, prompt_suffix)
        request = ChatCompletionsRequest(
            case_id=case_id,
            prompt=prompt,
            start_char="[",
            end_char="]",
            retries_left=1
        )

        return await self._openai_adapter.chat_completions(request)

    async def _generate_tracks_uris(self,
                                    artists_names: List[str],
                                    spotify_client: SpotifyClient,
                                    country: str) -> List[str]:
        artists_details = await self._artists_collector.collect(artists_names, spotify_client)  # TODO: Wrap spotify client with case progress reporting class
        relevant_artists = self._artists_filterer.filter_relevant_artists(artists_details)
        artists_ids = [artist[ID] for artist in relevant_artists]
        top_tracks = await spotify_client.artists.top_tracks.run(artists_ids, market=country)

        return self._extract_tracks_uris(top_tracks)

    @staticmethod
    def _extract_tracks_uris(tracks: List[Dict[str, List[dict]]]) -> List[str]:
        uris = []

        for artist_tracks in tracks:
            inner_tracks = artist_tracks.get(TRACKS, [])

            if inner_tracks:
                for track in inner_tracks:
                    uris.append(track[URI])

        return uris
