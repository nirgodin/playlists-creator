import asyncio
from typing import List

import pandas as pd
from pandas import DataFrame

from server.component_factory import get_openai_client
from server.consts.api_consts import NAME, ID
from server.consts.data_consts import URI
from server.consts.path_consts import TRACK_NAMES_EMBEDDINGS_PATH
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
        self._embeddings_database = pd.read_csv(TRACK_NAMES_EMBEDDINGS_PATH)
        self._similarity_scores_computer = SimilarityScoresComputer()

    async def select_tracks(self, text: str):
        prompt_embeddings = await self._openai_client.embeddings(text)
        embeddings_dataframe = self._transform_embeddings_to_dataframe(prompt_embeddings)
        similarity_scores = self._similarity_scores_computer.compute_similarity_scores(
            database=self._embeddings_database.drop(NON_EMBEDDINGS_COLUMNS, axis=1),
            candidate=embeddings_dataframe
        )
        data = self._embeddings_database.copy(deep=True)
        data[SIMILARITY_SCORE] = similarity_scores
        data.sort_values(by=SIMILARITY_SCORE, ascending=False, inplace=True)
        print('b')

    @staticmethod
    def _transform_embeddings_to_dataframe(embeddings: List[float]) -> DataFrame:
        record = {f'lyrics_embedding_{i + 1}': [embedding] for i, embedding in enumerate(embeddings)}
        return pd.DataFrame(record)


async def main(text: str):
    openai_client = await get_openai_client()
    selector = EmbeddingsTracksSelector(openai_client)

    return await selector.select_tracks(text)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main("two men that are a couple"))
