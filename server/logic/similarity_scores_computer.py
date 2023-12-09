from typing import List

import numpy as np
from numpy import ndarray
from pandas import DataFrame
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

from genie_common.tools.logs import logger


class SimilarityScoresComputer:
    def compute_similarity_scores(self, database: DataFrame, candidate: DataFrame) -> List[float]:
        logger.info("Starting to compute similarity scores")
        vectorized_candidate = self._vectorize(candidate).reshape(1, -1)
        vectorized_database = self._vectorize(database)
        scores = self._calculate_scores(vectorized_database, vectorized_candidate)
        logger.info("Finished computing similarity scores")

        return scores

    def _calculate_scores(self, database: ndarray, candidate: ndarray) -> List[float]:
        scores = []
        n_records = len(database)

        with tqdm(total=n_records) as progress_bar:
            for i in range(n_records):
                similarity = self._compute_single_similarity_score(candidate, database[i])
                scores.append(similarity)
                progress_bar.update(1)

        return scores

    @staticmethod
    def _vectorize(data: DataFrame) -> ndarray:
        sorted_columns_data = data[sorted(data.columns)]
        return sorted_columns_data.to_numpy()

    @staticmethod
    def _compute_single_similarity_score(vectorized_playlist: ndarray, database_row: ndarray) -> float:
        try:
            vectorized_database_row = database_row.reshape(1, -1)
            return cosine_similarity(vectorized_playlist, vectorized_database_row)[0][0]

        except:
            logger.exception("Failed to compute similarity score. Returning nan instead")
            return np.nan
