import json
from functools import lru_cache
from typing import Dict

from server.consts.path_consts import COLUMNS_DESCRIPTIONS_PATH
from server.utils.general_utils import titleize_feature_name


class FeaturesDescriptionsManager:
    @lru_cache
    def get_features_descriptions(self) -> Dict[str, str]:
        return {titleize_feature_name(k): v for k, v in self._features_descriptions.items()}

    @lru_cache
    def get_single_feature_description(self, feature_name: str) -> str:
        return self._features_descriptions[feature_name]

    @property
    def _features_descriptions(self) -> Dict[str, str]:
        with open(COLUMNS_DESCRIPTIONS_PATH, 'r') as f:
            return json.load(f)
