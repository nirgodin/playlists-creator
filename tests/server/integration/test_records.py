from dataclasses import dataclass
from typing import List

from genie_datastores.postgres.models import SpotifyArtist, ShazamArtist, Artist, SpotifyTrack, AudioFeatures, \
    TrackLyrics, RadioTrack
from genie_datastores.postgres.operations import insert_records
from sqlalchemy.ext.asyncio import AsyncEngine


@dataclass
class TestRecords:
    engine: AsyncEngine
    spotify_artists: List[SpotifyArtist]
    shazam_artists: List[ShazamArtist]
    artists: List[Artist]
    spotify_tracks: List[SpotifyTrack]
    radio_tracks: List[RadioTrack]
    audio_features: List[AudioFeatures]
    tracks_lyrics: List[TrackLyrics]

    async def insert(self):
        await insert_records(engine=self.engine, records=self.spotify_artists)
        await insert_records(engine=self.engine, records=self.shazam_artists)
        await insert_records(engine=self.engine, records=self.artists)
        await insert_records(engine=self.engine, records=self.spotify_tracks)
        await insert_records(engine=self.engine, records=self.radio_tracks)
        await insert_records(engine=self.engine, records=self.audio_features + self.tracks_lyrics)
