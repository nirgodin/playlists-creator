from typing import Dict, List

import pandas as pd
from genie_common.tools import SyncPoolExecutor
from genie_common.utils import chain_dicts, safe_nested_get
from pandas import DataFrame

from server.consts.data_consts import FOLLOWERS, TOTAL, ALBUM, ARTIST, NAME, \
    POPULARITY, RELEASE_DATE, RELEASE_YEAR
from server.data.track_features import TrackFeatures
from server.logic.playlist_imitation.playlist_imitator_consts import AUDIO_FEATURES_IRRELEVANT_KEYS, \
    ARTISTS_FEATURES_IRRELEVANT_KEYS, TRACKS_FEATURES_IRRELEVANT_KEYS, ALBUM_RELEVANT_FEATURES
from server.utils.data_utils import sort_data_columns_alphabetically
from server.utils.regex_utils import extract_year

ARTIST_REQUIRED_PREFIX_FEATURES = [
    NAME,
    POPULARITY,
    FOLLOWERS
]


class PlaylistDetailsSerializer:
    def __init__(self, pool_executor: SyncPoolExecutor = SyncPoolExecutor()):
        self._pool_executor = pool_executor

    def serialize(self, tracks_features: List[TrackFeatures]) -> DataFrame:
        serialized_details = self._pool_executor.run(
            iterable=tracks_features,
            func=self._serialize_single_track_features,
            expected_type=dict
        )
        data = pd.DataFrame.from_records(serialized_details)

        return sort_data_columns_alphabetically(data)

    def _serialize_single_track_features(self, track_features: TrackFeatures) -> dict:
        details = [
            self._serialize_audio_features(track_features.audio),
            self._serialize_track_features(track_features.track),
            self._serialize_artist_features(track_features.artist)
        ]
        return chain_dicts(*details)

    @staticmethod
    def _serialize_audio_features(audio_features: dict) -> Dict[str, float]:
        return {k: v for k, v in audio_features.items() if k not in AUDIO_FEATURES_IRRELEVANT_KEYS}

    def _serialize_track_features(self, track: dict) -> dict:
        track_features = self._extract_album_features(track)

        for k, v in track.items():
            if k not in TRACKS_FEATURES_IRRELEVANT_KEYS:
                track_features[k] = v

        return track_features

    def _extract_album_features(self, track: dict) -> dict:
        raw_album_features = track.get(ALBUM)

        if raw_album_features is None:
            return {}

        return self._serialize_album_features(raw_album_features)

    @staticmethod
    def _serialize_album_features(raw_album_features: dict) -> dict:
        album_features = {}

        for k, v in raw_album_features.items():
            if k not in ALBUM_RELEVANT_FEATURES:
                continue
            elif k == RELEASE_DATE:
                album_features[RELEASE_YEAR] = extract_year(v)
            else:
                album_features[k] = v

        return album_features

    @staticmethod
    def _serialize_artist_features(artist: dict) -> dict:
        artist_features = {}

        for k, v in artist.items():
            if k in ARTISTS_FEATURES_IRRELEVANT_KEYS:
                continue

            if k == FOLLOWERS:
                v = safe_nested_get(artist, [FOLLOWERS, TOTAL])

            if k in ARTIST_REQUIRED_PREFIX_FEATURES:
                artist_features[f'{ARTIST}_{k}'] = v
            else:
                artist_features[k] = v

        return artist_features
