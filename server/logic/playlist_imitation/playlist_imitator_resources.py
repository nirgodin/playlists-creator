from dataclasses import dataclass

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler


@dataclass
class PlaylistImitatorResources:
    imputer: SimpleImputer
    scaler: MinMaxScaler
    method: str
