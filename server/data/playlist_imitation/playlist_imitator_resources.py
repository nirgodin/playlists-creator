from dataclasses import dataclass

from sklearn.compose import ColumnTransformer


@dataclass
class PlaylistImitatorResources:
    pipeline: ColumnTransformer
    method: str
