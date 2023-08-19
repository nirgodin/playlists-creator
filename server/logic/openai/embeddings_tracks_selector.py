import pandas as pd

from server.consts.path_consts import TRACK_NAMES_EMBEDDINGS_PATH
from server.logic.openai.openai_client import OpenAIClient


class EmbeddingsTracksSelector:
    def __init__(self, openai_client: OpenAIClient):
        self._openai_client = openai_client
        self._embeddings_database = pd.read_csv(TRACK_NAMES_EMBEDDINGS_PATH)

    async def select_tracks(self, text: str):
        prompt_embeddings = await self._openai_client.embeddings(text)

