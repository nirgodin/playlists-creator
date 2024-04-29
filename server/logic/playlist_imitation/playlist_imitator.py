from typing import List

from sklearn.compose import ColumnTransformer

from server.data.track_features import TrackFeatures
from server.logic.playlist_imitation.playlist_details_serializer import PlaylistDetailsSerializer
from server.logic.playlist_imitation.playlist_imitator_tracks_selector import PlaylistImitatorTracksSelector


class PlaylistImitator:
    def __init__(self,
                 tracks_selector: PlaylistImitatorTracksSelector,
                 column_transformer: ColumnTransformer,
                 playlist_details_serializer: PlaylistDetailsSerializer = PlaylistDetailsSerializer()):
        self._playlist_details_serializer = playlist_details_serializer
        self._column_transformer = column_transformer
        self._tracks_selector = tracks_selector

    def imitate_playlist(self, tracks_features: List[TrackFeatures]) -> List[str]:
        serialized_playlist_data = self._playlist_details_serializer.serialize(tracks_features)
        transformed_playlist_data = self._column_transformer.transform(serialized_playlist_data)

        return self._tracks_selector.select_tracks(transformed_playlist_data)  # TODO: Think how to do this
