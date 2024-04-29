from typing import List

from genie_datastores.milvus import MilvusClient
from genie_datastores.milvus.models import SearchRequest
from sklearn.compose import ColumnTransformer

from server.consts.api_consts import ID
from server.data.track_features import TrackFeatures
from server.logic.playlist_imitation.playlist_details_serializer import PlaylistDetailsSerializer


class PlaylistImitator:
    def __init__(self,
                 column_transformer: ColumnTransformer,
                 milvus_client: MilvusClient,
                 playlist_details_serializer: PlaylistDetailsSerializer = PlaylistDetailsSerializer()):
        self._playlist_details_serializer = playlist_details_serializer
        self._column_transformer = column_transformer
        self._milvus_client = milvus_client

    async def imitate(self, tracks_features: List[TrackFeatures]) -> List[str]:
        serialized_playlist_data = self._playlist_details_serializer.serialize(tracks_features)
        transformed_playlist_data = self._column_transformer.transform(serialized_playlist_data)
        playlist_vector = transformed_playlist_data.median(axis=0)

        return await self._search_features_db_for_nearest_neighbors(playlist_vector)

    async def _search_features_db_for_nearest_neighbors(self, playlist_vector: List[float]) -> List[str]:
        request = SearchRequest(
            collection_name="tracks_features",
            vector=playlist_vector,
        )
        response = await self._milvus_client.vectors.search(request)  # TODO: Integrate here distance threshold

        return [track[ID] for track in response]
