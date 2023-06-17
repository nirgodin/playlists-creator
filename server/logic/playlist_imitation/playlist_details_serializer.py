import json
from typing import Dict, List, Callable, Optional, Any

import pandas as pd
from pandas import DataFrame

from server.consts.data_consts import FOLLOWERS, TOTAL, ALBUM, TRACKS, ARTISTS, AUDIO_FEATURES, TRACK, ARTIST, NAME, \
    POPULARITY
from server.logic.playlist_imitation.playlist_imitator_consts import AUDIO_FEATURES_IRRELEVANT_KEYS, \
    ARTISTS_FEATURES_IRRELEVANT_KEYS, TRACKS_FEATURES_IRRELEVANT_KEYS, ALBUM_RELEVANT_FEATURES
from server.utils.general_utils import chain_dicts

ARTIST_REQUIRED_PREFIX_FEATURES = [
    NAME,
    POPULARITY,
    FOLLOWERS
]
ALBUM_REQUIRED_PREFIX_FEATURES = [
    NAME
]


class PlaylistDetailsSerializer:
    def serialize(self, playlist_details: Dict[str, List[dict]]) -> DataFrame:
        serialized_details = []

        for i in range(len(playlist_details[TRACKS])):
            details = [
                self._serialize_single_track_audio_features(playlist_details[AUDIO_FEATURES][i]),
                self._serialize_single_track_features(playlist_details[TRACKS][i]),
                self._serialize_single_artist_features(playlist_details[ARTISTS][i])
            ]
            serialized_track_details = chain_dicts(details)
            serialized_details.append(serialized_track_details)

        return pd.DataFrame.from_records(serialized_details)

    @staticmethod
    def _serialize_single_track_audio_features(audio_features: dict) -> Dict[str, float]:
        return {k: v for k, v in audio_features.items() if k not in AUDIO_FEATURES_IRRELEVANT_KEYS}

    def _serialize_single_track_features(self, track: dict) -> dict:
        track_features = self._extract_album_features(track)

        for k, v in track.items():
            if k in TRACKS_FEATURES_IRRELEVANT_KEYS:
                continue
            else:
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
            elif k in ALBUM_REQUIRED_PREFIX_FEATURES:
                album_features[f'{ALBUM}_{k}'] = v
            else:
                album_features[k] = v

        return album_features

    def _serialize_single_artist_features(self, artist: dict) -> dict:
        artist_features = {}

        for k, v in artist.items():
            if k in ARTISTS_FEATURES_IRRELEVANT_KEYS:
                continue

            if k in self._artists_features_to_extraction_methods_mapping.keys():
                extraction_method = self._artists_features_to_extraction_methods_mapping[k]
                v = extraction_method(artist)

            if k in ARTIST_REQUIRED_PREFIX_FEATURES:
                artist_features[f'{ARTIST}_{k}'] = v
            else:
                artist_features[k] = v

        return artist_features

    @staticmethod
    def _extract_artist_followers(artist_features: dict) -> Optional[int]:
        return artist_features.get(FOLLOWERS, {}).get(TOTAL)

    @property
    def _artists_features_to_extraction_methods_mapping(self) -> Dict[str, Callable]:
        return {
            FOLLOWERS: self._extract_artist_followers
        }


if __name__ == '__main__':
    with open('/Users/nirgodin/Downloads/playlist_details_sample.json', 'r') as f:
        raw_details = json.load(f)

    PlaylistDetailsSerializer().serialize(raw_details)
