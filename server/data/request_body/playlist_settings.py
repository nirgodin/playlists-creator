from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PlaylistSettings:
    playlist_name: str = ""
    playlist_description: str = ""
    is_public: bool = False
    prompt: str = ""
    existing_playlist: str = ""
    time_range: str = ""
