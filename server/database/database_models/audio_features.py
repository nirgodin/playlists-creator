from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class AudioFeatures:
    acousticness: float
    danceability: float
    duration_ms: int
    energy: float
    instrumentalness: float
    key: int
    liveness: float
    loudness: float
    mode: bool
    speechiness: float
    tempo: float
    time_signature: int
    valence: float
