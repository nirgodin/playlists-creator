from typing import List

import pandas as pd
from pandas import DataFrame

from server.consts.api_consts import NAME, ID
from server.consts.data_consts import URI
from server.logic.openai.openai_client import OpenAIClient
from server.logic.playlist_imitation.playlist_imitator_consts import SIMILARITY_SCORE
from server.logic.similarity_scores_computer import SimilarityScoresComputer

NON_EMBEDDINGS_COLUMNS = [
    NAME,
    ID,
    URI
]
EMBEDDINGS_SIMILARITY_SCORE_THRESHOLD = 0.78


class EmbeddingsTracksSelector:
    def __init__(self, openai_client: OpenAIClient):
        self._openai_client = openai_client
        self._similarity_scores_computer = SimilarityScoresComputer()

    async def select_tracks(self, embeddings_data: DataFrame, text: str) -> List[str]:
        prompt_embeddings = await self._openai_client.embeddings(text)
        embeddings_dataframe = self._transform_embeddings_to_dataframe(prompt_embeddings)
        similarity_scores = self._similarity_scores_computer.compute_similarity_scores(
            database=embeddings_data.drop(NON_EMBEDDINGS_COLUMNS, axis=1),
            candidate=embeddings_dataframe
        )
        embeddings_data[SIMILARITY_SCORE] = similarity_scores
        relevant_data = embeddings_data[embeddings_data[SIMILARITY_SCORE] > EMBEDDINGS_SIMILARITY_SCORE_THRESHOLD]
        relevant_data.sort_values(by=SIMILARITY_SCORE, ascending=False, inplace=True)

        return relevant_data[URI].tolist()

    @staticmethod
    def _transform_embeddings_to_dataframe(embeddings: List[float]) -> DataFrame:
        record = {f'lyrics_embedding_{i + 1}': [embedding] for i, embedding in enumerate(embeddings)}
        return pd.DataFrame(record)
