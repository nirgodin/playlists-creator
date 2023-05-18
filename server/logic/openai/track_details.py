from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class TrackDetails:
    track_name: str
    artist_name: str

    def __post_init__(self):
        self.query = f'{self.artist_name} {self.track_name}'
