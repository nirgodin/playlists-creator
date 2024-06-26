from enum import Enum


class CaseStatus(Enum):
    CREATED = "created"
    COMPLETED = "completed"
    COVER = "cover"
    PHOTO = "photo"
    PLAYLIST = "playlist"
    PLAYLIST_DETAILS = "playlist_details"
    PROMPT = "prompt"
    TEXTUAL_QUERY = "textual_query"
    TRACKS = "tracks"
