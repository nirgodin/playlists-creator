from typing import List

from server.data.content_controllers.base_request import BaseRequest


class PlaylistsMergerRequest(BaseRequest):
    ids: List[str]
    shuffle: bool
    cover_photo_prompt: str
