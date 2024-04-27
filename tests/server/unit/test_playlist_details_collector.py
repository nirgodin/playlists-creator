from http import HTTPStatus
from random import shuffle, randint
from typing import List

from _pytest.fixtures import fixture
from aioresponses import aioresponses
from genie_common.tools import AioPoolExecutor
from spotipyio import SpotifyClient

from server.consts.api_consts import ID
from server.consts.data_consts import ARTISTS
from server.data.track_features import TrackFeatures
from server.logic.data_collection.spotify_playlist_details_collector import PlaylistDetailsCollector
from tests.server.utils import random_spotify_id, build_spotify_url


class TestPlaylistDetailsCollector:
    async def test_collect__empty_playlist__returns_empty_list(self,
                                                               collector: PlaylistDetailsCollector,
                                                               spotify_client: SpotifyClient):
        actual = await collector.collect([], spotify_client)
        assert actual == []

    async def test_collect__non_empty_playlist__returns_tracks_features_list(self,
                                                                             collector: PlaylistDetailsCollector,
                                                                             spotify_client: SpotifyClient,
                                                                             tracks: List[dict],
                                                                             expected: List[TrackFeatures]):
        actual = await collector.collect(tracks, spotify_client)
        assert sorted(actual, key=lambda x: x.track[ID]) == sorted(expected, key=lambda x: x.track[ID])

    @fixture(scope="class")
    def collector(self) -> PlaylistDetailsCollector:
        pool_executor = AioPoolExecutor()
        return PlaylistDetailsCollector(pool_executor)

    @fixture(scope="function")
    def tracks(self,
               valid_tracks: List[dict],
               invalid_audio_response_tracks: List[dict],
               invalid_arist_response_tracks: List[dict]):
        tracks = valid_tracks + invalid_audio_response_tracks + invalid_arist_response_tracks
        shuffle(tracks)

        yield tracks

    @fixture(scope="function")
    def valid_tracks(self, mock_responses: aioresponses) -> List[dict]:
        tracks = self._some_random_tracks(min_length=1)

        for track in tracks:
            self._given_valid_artist_response(mock_responses, track)
            self._given_valid_audio_response(mock_responses, track)

        yield tracks

    @fixture(scope="function")
    def invalid_audio_response_tracks(self, mock_responses: aioresponses) -> List[dict]:
        tracks = self._some_random_tracks(min_length=1)

        for track in tracks:
            self._given_valid_artist_response(mock_responses, track)
            self._given_invalid_audio_response(mock_responses, track)

        yield tracks

    @fixture(scope="function")
    def invalid_arist_response_tracks(self, mock_responses: aioresponses) -> List[dict]:
        tracks = self._some_random_tracks(min_length=1)

        for track in tracks:
            self._given_invalid_artist_response(mock_responses, track)
            self._given_valid_audio_response(mock_responses, track)

        yield tracks

    @fixture(scope="function")
    def expected(self, valid_tracks: List[dict]) -> List[TrackFeatures]:
        features = []

        for track in valid_tracks:
            track_features = TrackFeatures(
                track=track,
                artist={ID: track[ARTISTS][0][ID]},
                audio={ID: track[ID]}
            )
            features.append(track_features)

        yield features

    def _some_random_tracks(self, min_length: int = 0, max_length: int = 10) -> List[dict]:
        tracks_number = randint(min_length, max_length)
        return [self._random_track() for _ in range(tracks_number)]

    @staticmethod
    def _random_track() -> dict:
        return {
            ID: random_spotify_id(),
            ARTISTS: [
                {ID: random_spotify_id()}
            ]
        }

    def _given_valid_audio_response(self, mock_responses: aioresponses, track: dict) -> None:
        mock_responses.get(
            url=self._build_audio_features_url(track),
            payload={"audio_features": [{ID: track[ID]}]}
        )

    def _given_valid_artist_response(self, mock_responses: aioresponses, track: dict) -> None:
        artist_id = track[ARTISTS][0][ID]
        mock_responses.get(
            url=self._build_artists_url(track),
            payload={ARTISTS: [{ID: artist_id}]}
        )

    def _given_invalid_audio_response(self, mock_responses: aioresponses, track: dict) -> None:
        mock_responses.get(
            url=self._build_audio_features_url(track),
            status=HTTPStatus.BAD_REQUEST.value
        )

    def _given_invalid_artist_response(self, mock_responses: aioresponses, track: dict) -> None:
        mock_responses.get(
            url=self._build_artists_url(track),
            status=HTTPStatus.BAD_REQUEST.value
        )

    @staticmethod
    def _build_audio_features_url(track: dict) -> str:
        track_id = track[ID]
        return build_spotify_url(routes=["audio-features"], params={"ids": track_id})

    @staticmethod
    def _build_artists_url(track: dict) -> str:
        artist_id = track[ARTISTS][0][ID]
        return build_spotify_url(routes=[ARTISTS], params={"ids": artist_id})
