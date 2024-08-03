from http import HTTPStatus
from random import randint, shuffle
from typing import Dict, List

from _pytest.fixtures import fixture
from aioresponses import aioresponses
from genie_common.utils import random_string_array, chain_lists
from spotipyio import SpotifyClient

from server.consts.data_consts import PLAYLISTS
from server.logic.playlists_merger import PlaylistsMerger
from tests.server.utils import some_tracks_uris, build_spotify_url, build_playlist_response


class TestPlaylistsMerger:
    async def test_merge__shuffle_false__returns_ordered_chained_uris(self,
                                                                      spotify_client: SpotifyClient,
                                                                      mock_responses: aioresponses,
                                                                      playlists_ids_uris_map: Dict[str, List[str]],
                                                                      expected_uris: List[str]):
        self._given_valid_playlists_info_responses(mock_responses, playlists_ids_uris_map)
        playlists_ids = list(playlists_ids_uris_map.keys())

        actual = await PlaylistsMerger.merge(
            spotify_client=spotify_client, ids=playlists_ids, shuffle_items=False
        )

        assert actual == expected_uris

    async def test_merge__shuffle_true__returns_unordered_chained_uris(self,
                                                                       spotify_client: SpotifyClient,
                                                                       mock_responses: aioresponses,
                                                                       playlists_ids_uris_map: Dict[str, List[str]],
                                                                       expected_uris: List[str]):
        self._given_valid_playlists_info_responses(mock_responses, playlists_ids_uris_map)
        playlists_ids = list(playlists_ids_uris_map.keys())

        actual = await PlaylistsMerger.merge(
            spotify_client=spotify_client, ids=playlists_ids, shuffle_items=True
        )

        assert actual != expected_uris
        assert sorted(actual) == sorted(expected_uris)

    async def test_merge__all_playlists_responses_invalid__returns_empty_list(self,
                                                                              spotify_client: SpotifyClient,
                                                                              invalid_playlists_ids: List[str],
                                                                              mock_responses: aioresponses):
        self._given_invalid_playlists_info_responses(mock_responses, invalid_playlists_ids)
        actual = await PlaylistsMerger.merge(
            spotify_client=spotify_client, ids=invalid_playlists_ids
        )
        assert actual == []

    async def test_merge__some_playlists_responses_invalid__returns_only_valid_playlists_uris(
        self,
        spotify_client: SpotifyClient,
        mock_responses: aioresponses,
        invalid_playlists_ids: List[str],
        playlists_ids_uris_map: Dict[str, List[str]],
        expected_uris: List[str],
    ):
        self._given_invalid_playlists_info_responses(mock_responses, invalid_playlists_ids)
        self._given_valid_playlists_info_responses(mock_responses, playlists_ids_uris_map)
        valid_playlists_ids = list(playlists_ids_uris_map.keys())
        ids = valid_playlists_ids + invalid_playlists_ids
        shuffle(ids)

        actual = await PlaylistsMerger.merge(
            spotify_client=spotify_client, ids=ids, shuffle_items=False
        )

        assert sorted(actual) == sorted(expected_uris)

    @fixture
    def playlists_ids_uris_map(self) -> Dict[str, List[str]]:
        playlists_ids = random_string_array(length=randint(1, 10))
        playlists_map = {}

        for id_ in playlists_ids:
            playlists_map[id_] = some_tracks_uris()

        return playlists_map

    @fixture
    def invalid_playlists_ids(self) -> List[str]:
        return random_string_array()

    @fixture
    def expected_uris(self, playlists_ids_uris_map: Dict[str, List[str]]) -> List[str]:
        return chain_lists(list(playlists_ids_uris_map.values()))

    @staticmethod
    def _given_valid_playlists_info_responses(mock_responses: aioresponses,
                                              playlists_ids_uris_map: Dict[str, List[str]]) -> None:
        for playlist_id, expected_uris in playlists_ids_uris_map.items():
            mock_responses.get(
                url=build_spotify_url([PLAYLISTS, playlist_id]),  # TODO: Extract to consts
                payload=build_playlist_response(expected_uris)
            )

    @staticmethod
    def _given_invalid_playlists_info_responses(mock_responses: aioresponses, playlists_ids: List[str]) -> None:
        for playlist_id in playlists_ids:
            mock_responses.get(
                url=build_spotify_url([PLAYLISTS, playlist_id]),  # TODO: Extract to consts
                status=HTTPStatus.BAD_REQUEST.value
            )
