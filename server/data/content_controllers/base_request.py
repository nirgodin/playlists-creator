from server.data.content_controllers.base_genie_model import BaseGenieModel
from server.data.content_controllers.playlist_metadata import PlaylistMetadata


class BaseRequest(BaseGenieModel):
    access_code: str
    playlist_details: PlaylistMetadata  # TODO: Rename field_name to metadata once integrated in all controllers
