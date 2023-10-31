from dataclasses import dataclass
from typing import Optional, List

from dataclasses_json import dataclass_json
from postgres_client.models.enum.gender import Gender


@dataclass_json
@dataclass
class Artist:
    artist_id: str
    gender: Optional[Gender]
    genres: Optional[List[str]]
    primary_genre: Optional[str]
    is_israeli: Optional[bool]
