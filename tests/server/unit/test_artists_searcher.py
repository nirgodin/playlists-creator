from logging import WARNING
from random import shuffle
from typing import List, Dict, Optional, Callable, Any

from _pytest.fixtures import fixture
from _pytest.logging import LogCaptureFixture
from aiohttp import ClientError
from aioresponses import aioresponses
from genie_common.utils import random_string_dict, random_alphanumeric_string
from spotipyio import SpotifyClient

from server.consts.data_consts import ARTISTS, ITEMS, NAME
from server.logic.ocr.artists_searcher import ArtistsSearcher
from tests.server.utils import build_spotify_url, assert_expected_level_logs_count, build_artists_search_response


class TestArtistsSearcher:
    async def test_search(self,
                          artists_searcher: ArtistsSearcher,
                          artists_names: List[str],
                          spotify_client: SpotifyClient,
                          expected: List[Dict[str, str]],
                          mock_responses: aioresponses,
                          invalid_responses_artists: Dict[str, str],
                          exception_artists: Dict[str, str],
                          caplog: LogCaptureFixture):
        with caplog.at_level(WARNING):
            actual = await artists_searcher.search(artists_names, spotify_client)

        assert sorted(actual) == sorted(expected)
        assert len(mock_responses.requests) == len(artists_names)
        assert_expected_level_logs_count(caplog, level="WARNING", expected=len(invalid_responses_artists))
        assert_expected_level_logs_count(caplog, level="ERROR", expected=len(exception_artists))

    @fixture(scope="function")
    def artists_names(self,
                      found_artists: Dict[str, str],
                      not_found_artists: Dict[str, str],
                      not_matched_artists: Dict[str, str],
                      invalid_responses_artists: Dict[str, str],
                      exception_artists: Dict[str, str]) -> List[str]:
        artists = (
            list(found_artists.values()) +
            list(not_found_artists.values()) +
            list(not_matched_artists.values()) +
            list(invalid_responses_artists.values()) +
            list(exception_artists.values())
        )
        shuffle(artists)

        return artists

    @fixture(scope="function")
    def found_artists(self, mock_responses: aioresponses) -> Dict[str, str]:
        artists = self._random_artists_ids_names_mapping()
        self._set_artists_responses(
            artists=artists,
            mock_responses=mock_responses,
            payload_func=build_artists_search_response
        )

        return artists

    @fixture(scope="function")
    def expected(self, found_artists: Dict[str, str]) -> List[str]:
        return list(found_artists.keys())

    @staticmethod
    def _random_artists_ids_names_mapping() -> Dict[str, str]:
        artists = random_string_dict()
        return {id_: name for id_, name in artists.items() if id_ and name}

    @fixture(scope="function")
    def not_found_artists(self, mock_responses: aioresponses) -> Dict[str, str]:
        artists = self._random_artists_ids_names_mapping()
        self._set_artists_responses(
            artists=artists,
            mock_responses=mock_responses,
            payload_func=lambda artist_id, artist_name: {
                ARTISTS: {
                    ITEMS: []
                }
            }
        )

        return artists

    @fixture(scope="function")
    def not_matched_artists(self, mock_responses: aioresponses) -> Dict[str, str]:
        artists = self._random_artists_ids_names_mapping()
        self._set_artists_responses(
            artists=artists,
            mock_responses=mock_responses,
            payload_func=lambda artist_id, artist_name: {
                ARTISTS: {
                    ITEMS: [
                        {NAME: random_alphanumeric_string()}
                    ]
                }
            }
        )

        return artists

    @fixture(scope="function")
    def invalid_responses_artists(self, mock_responses: aioresponses) -> Dict[str, str]:
        artists = self._random_artists_ids_names_mapping()
        self._set_artists_responses(
            artists=artists,
            mock_responses=mock_responses,
            payload_func=lambda artist_id, artist_name: []
        )

        return artists

    @fixture(scope="function")
    def exception_artists(self, mock_responses: aioresponses) -> Dict[str, str]:
        artists = self._random_artists_ids_names_mapping()
        self._set_artists_responses(
            artists=artists,
            mock_responses=mock_responses,
            exception=ClientError()
        )

        return artists

    @staticmethod
    def _set_artists_responses(artists: Dict[str, str],
                               mock_responses: aioresponses,
                               payload_func: Optional[Callable[[str, str], Any]] = None,
                               exception: Optional[Exception] = None) -> None:
        for artist_id, artist_name in artists.items():
            params = {"limit": "50", "offset": "0", "q": f"artist:{artist_name}", "type": "artist"}
            url = build_spotify_url(["search"], params)

            if exception is not None:
                mock_responses.get(url=url, exception=exception)
            else:
                mock_responses.get(url=url, payload=payload_func(artist_id, artist_name))

    @staticmethod
    def _assert_expected_warning_logs(caplog: LogCaptureFixture, artists: Dict[str, str]):
        warning_records = [record for record in caplog.records if record.levelname == "WARNING"]
        assert len(warning_records) == len(artists)

    @staticmethod
    def _assert_expected_exception_logs(caplog: LogCaptureFixture, artists: Dict[str, str]):
        error_records = [record for record in caplog.records if record.levelname == "ERROR"]
        assert len(error_records) == len(artists)
