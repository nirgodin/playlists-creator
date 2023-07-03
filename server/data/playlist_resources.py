from dataclasses import dataclass
from typing import Optional, List


@dataclass
class PlaylistResources:
    uris: Optional[List[str]]
    cover_image_path: Optional[str]
