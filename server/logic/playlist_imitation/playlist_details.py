from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class PlaylistDetails:
    tracks: List[dict]
    artists: List[dict]
    audio_features: List[dict]
    cover_image_url: Optional[str]
