from typing import Optional

from genie_common.models.openai import ImageSize
from genie_common.openai import OpenAIClient
from spotipyio import SpotifyClient
from spotipyio.logic.collectors.search_collectors.spotify_search_type import SpotifySearchType

from server.consts.app_consts import FILTER_PARAMS
from server.controllers.content_controllers.base_content_controller import BaseContentController
from server.data.playlist_resources import PlaylistResources
from server.logic.configuration_photo_prompt.configuration_photo_prompt_creator import ConfigurationPhotoPromptCreator
from server.logic.database_client import DatabaseClient
from server.logic.parameters_transformer import ParametersTransformer
from server.logic.playlists_creator import PlaylistsCreator
from server.tools.authenticator import Authenticator
from server.utils.image_utils import current_timestamp_image_path
from server.utils.spotify_utils import sample_uris, to_uris


class ConfigurationController(BaseContentController):
    def __init__(self,
                 authenticator: Authenticator,
                 playlists_creator: PlaylistsCreator,
                 openai_client: OpenAIClient,
                 photo_prompt_creator: ConfigurationPhotoPromptCreator,
                 db_client: DatabaseClient,
                 parameters_transformer: ParametersTransformer = ParametersTransformer()):
        super().__init__(authenticator, playlists_creator, openai_client)
        self._photo_prompt_creator = photo_prompt_creator
        self._db_client = db_client
        self._parameters_transformer = parameters_transformer

    async def _generate_playlist_resources(self,
                                           request_body: dict,
                                           dir_path: str,
                                           spotify_client: SpotifyClient) -> PlaylistResources:
        query_conditions = self._parameters_transformer.transform(request_body)
        tracks_ids = await self._db_client.query(query_conditions)
        tracks_uris = to_uris(SpotifySearchType.TRACK, *tracks_ids)

        return PlaylistResources(
            uris=sample_uris(tracks_uris),
            cover_image_path=current_timestamp_image_path(dir_path)
        )

    async def _generate_playlist_cover(self, request_body: dict, image_path: str) -> Optional[str]:
        filter_params = request_body[FILTER_PARAMS]
        playlist_cover_prompt = await self._photo_prompt_creator.create_prompt(filter_params)

        return await self._openai_client.images_generation.collect(
            prompt=playlist_cover_prompt,
            n=1,
            size=ImageSize.P512
        )
