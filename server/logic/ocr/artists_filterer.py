from difflib import SequenceMatcher
from typing import List

from server.consts.data_consts import ORIGINAL_INPUT, NAME


class ArtistsFilterer:
    def filter_relevant_artists(self, artists_details: List[dict], relevance_threshold: float = 0.8) -> List[dict]:
        relevant_artists = []

        for artist in artists_details:
            relevance_ratio = self._calculate_single_artist_relevance(artist)

            if relevance_ratio >= relevance_threshold:
                relevant_artists.append(artist)

        return relevant_artists

    def _calculate_single_artist_relevance(self, artist: dict) -> float:
        original_input = artist[ORIGINAL_INPUT].lower()
        result_name = artist[NAME].lower()

        return self._calculate_similarity_score(original_input, result_name)

    @staticmethod
    def _calculate_similarity_score(original_input: str, result_name: str) -> float:
        return SequenceMatcher(None, original_input, result_name).ratio()
