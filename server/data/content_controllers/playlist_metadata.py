from server.data.content_controllers.base_genie_model import BaseGenieModel


class PlaylistMetadata(BaseGenieModel):
    playlist_name: str
    playlist_description: str
    is_public: bool
