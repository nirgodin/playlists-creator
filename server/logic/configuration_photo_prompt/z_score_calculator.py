import json
from typing import Dict

from server.consts.path_consts import COLUMNS_Z_SCORES_METADATA_PATH
from server.data.column_z_score_metadata import ColumnZScoreMetadata
from server.utils.statistics_utils import calculate_z_score


class ZScoreCalculator:
    def calculate(self, value: float, column_name: str):
        column_metadata = self._z_scores_metadata[column_name]
        return calculate_z_score(value, column_metadata.mean, column_metadata.std)

    @property
    def _z_scores_metadata(self) -> Dict[str, ColumnZScoreMetadata]:
        with open(COLUMNS_Z_SCORES_METADATA_PATH, 'r') as f:
            raw_metadata = json.load(f)

        return {column: ColumnZScoreMetadata.from_dict(metadata) for column, metadata in raw_metadata.items()}
