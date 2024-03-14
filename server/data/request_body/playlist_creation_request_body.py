from dataclasses import dataclass
from typing import Dict, List

from dataclasses_json import dataclass_json, LetterCase

from server.data.request_body.filter_param import FilterParam
from server.data.request_body.playlist_settings import PlaylistSettings


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PlaylistCreationRequestBody:
    filter_params: Dict[str, FilterParam]
    playlist_details: PlaylistSettings
    features_names: Dict[str, List[str]]
    features_values: Dict[str, Dict[str, List[str]]]
    features_descriptions: Dict[str, str]
    access_code: str = ""
