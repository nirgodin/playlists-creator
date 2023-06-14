import json
from typing import Dict, List, Callable, Optional

import pandas as pd
from pandas import DataFrame

from server.consts.data_consts import FOLLOWERS, TOTAL, ALBUM, TRACKS, ARTISTS, AUDIO_FEATURES
from server.utils.general_utils import chain_dicts

AUDIO_FEATURES_IRRELEVANT_KEYS = [
    'type',
    'id',
    'uri',
    'track_href',
    'analysis_url',
    'type'
]

ARTISTS_FEATURES_IRRELEVANT_KEYS = [
    'external_urls',
    'href',
    'id',
    'uri',
    'images',
    'type'
]

TRACKS_FEATURES_IRRELEVANT_KEYS = [
    'artists',
    'available_markets',
    'duration_ms',
    'episode',
    'external_ids',
    'external_urls',
    'href',
    'id',
    'track',
    'preview_url',
    'album',
    'images',
    'type',
    'analysis_url',
    'track_href'
]

ALBUM_RELEVANT_FEATURES = [
    'name',
    'release_date',
    'total_tracks'
]


class PlaylistDetailsSerializer:
    def serialize(self, playlist_details: Dict[str, List[dict]]) -> DataFrame:
        serialized_details = []

        for i in range(len(playlist_details[TRACKS])):
            track_details = self._serialize_single_track_features(playlist_details[TRACKS][i])
            artist_details = self._serialize_single_artist_features(playlist_details[ARTISTS][i])
            audio_features_details = self._serialize_single_track_features(playlist_details[AUDIO_FEATURES][i])
            serialized_track_details = chain_dicts([track_details, artist_details, audio_features_details])
            serialized_details.append(serialized_track_details)

        data = pd.DataFrame.from_records(serialized_details)
        print('b')

    @staticmethod
    def _serialize_single_track_audio_features(audio_features: dict) -> Dict[str, float]:
        return {f'audio_features_{k}': v for k, v in audio_features.items() if k not in AUDIO_FEATURES_IRRELEVANT_KEYS}

    def _serialize_single_artist_features(self, artist: dict) -> dict:
        artist_features = {}

        for k, v in artist.items():
            if k in ARTISTS_FEATURES_IRRELEVANT_KEYS:
                continue
            elif k in self._artists_features_to_extraction_methods_mapping.keys():
                extraction_method = self._artists_features_to_extraction_methods_mapping[k]
                artist_features[f'artist_{k}'] = extraction_method(artist)
            else:
                artist_features[f'artist_{k}'] = v

        return artist_features

    def _serialize_single_track_features(self, track: dict) -> dict:
        track_features = self._extract_album_features(track)

        for k, v in track.items():
            if k in TRACKS_FEATURES_IRRELEVANT_KEYS:
                continue
            else:
                track_features[f'track_{k}'] = v

        return track_features

    @staticmethod
    def _extract_album_features(track: dict) -> dict:
        album_features = track.get(ALBUM)

        if album_features is None:
            return {}

        return {f'album_{k}': v for k, v in album_features.items() if k in ALBUM_RELEVANT_FEATURES}

    @staticmethod
    def _extract_artist_followers(artist_features: dict) -> Optional[int]:
        return artist_features.get(FOLLOWERS, {}).get(TOTAL)

    @property
    def _artists_features_to_extraction_methods_mapping(self) -> Dict[str, Callable]:
        return {
            'followers': self._extract_artist_followers
        }


if __name__ == '__main__':
    with open('/Users/nirgodin/Downloads/playlist_details_sample.json', 'r') as f:
        details = json.load(f)

    PlaylistDetailsSerializer().serialize(details)
