from typing import List

from genie_common.tools import logger
from genie_common.utils import compute_similarity_score

from server.consts.data_consts import ORIGINAL_INPUT, NAME


class ArtistsFilterer:
    def filter_relevant_artists(self, artists_details: List[dict], relevance_threshold: float = 0.8) -> List[dict]:
        logger.info("Filtering relevant artists")
        relevant_artists = []

        for artist in artists_details:
            relevance_ratio = self._calculate_single_artist_relevance(artist)

            if relevance_ratio >= relevance_threshold:
                relevant_artists.append(artist)

        return relevant_artists

    @staticmethod
    def _calculate_single_artist_relevance(artist: dict) -> float:
        original_input = artist[ORIGINAL_INPUT].lower()
        result_name = artist[NAME].lower()

        return compute_similarity_score(original_input, result_name)
