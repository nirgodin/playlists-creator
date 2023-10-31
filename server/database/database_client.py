import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Type

from dataclasses_json import dataclass_json
from postgres_client.models.enum.gender import Gender
from postgres_client.models.orm.audio_features import AudioFeatures as AudioFeaturesDB
from postgres_client.models.orm.base_orm_model import BaseORMModel
from postgres_client.models.orm.spotify_artist import SpotifyArtist
from postgres_client.models.orm.spotify_track import SpotifyTrack
from postgres_client.models.orm.track_lyrics import TrackLyrics
from postgres_client.postgres_operations import execute_query
from sqlalchemy import select, Row, inspect, Column
from sqlalchemy.ext.asyncio import AsyncEngine

from server.component_factory import get_database_engine
from server.consts.api_consts import ID
from server.consts.data_consts import RELEASE_DATE, EXPLICIT


@dataclass_json
@dataclass
class AudioFeatures:
    acousticness: float
    danceability: float
    duration_ms: int
    energy: float
    instrumentalness: float
    key: int
    liveness: float
    loudness: float
    mode: bool
    speechiness: float
    tempo: float
    time_signature: int
    valence: float


@dataclass_json
@dataclass
class Artist:
    artist_id: str
    gender: Optional[Gender]
    genres: Optional[List[str]]
    primary_genre: Optional[str]
    is_israeli: Optional[bool]


@dataclass_json
@dataclass
class Lyrics:
    language: Optional[str]


@dataclass_json
@dataclass
class Song:
    id: str
    explicit: bool
    release_date: datetime
    audio_features: AudioFeatures
    lyrics: Lyrics
    artist: Artist

    def __post_init__(self):
        self.release_year = self.release_date.year

    @classmethod
    def from_row(cls, row: Row) -> "Song":
        jsonified_row = dict(row._mapping)
        return cls(
            id=jsonified_row[ID],
            release_date=jsonified_row[RELEASE_DATE],
            explicit=jsonified_row[EXPLICIT],
            audio_features=AudioFeatures.from_dict(jsonified_row),
            lyrics=Lyrics.from_dict(jsonified_row),
            artist=Artist.from_dict(jsonified_row)
        )


def get_orm_columns(orm: Type[BaseORMModel]) -> List[Column]:
    return [column for column in inspect(orm).c]


def get_all_columns_except(orm: Type[BaseORMModel], *exclude_columns: List[Column]) -> List[Column]:
    columns = get_orm_columns(orm)
    return [col for col in columns if col not in exclude_columns]


class DatabaseClient:
    def __init__(self, db_engine: AsyncEngine):
        self._db_engine = db_engine

    async def query(self):
        audio_features_columns = get_all_columns_except(AudioFeaturesDB, AudioFeaturesDB.creation_date, AudioFeaturesDB.update_date)
        artist_columns = [
            SpotifyArtist.id.label(SpotifyTrack.artist_id.key),
            SpotifyArtist.gender,
            SpotifyArtist.genres,
            SpotifyArtist.primary_genre,
            SpotifyArtist.is_israeli,
        ]
        track_columns = [
            SpotifyTrack.id,
            SpotifyTrack.artist_id,
            SpotifyTrack.explicit,
            SpotifyTrack.release_date,
            # TODO: Add duration to ORM and database
        ]
        query = select(SpotifyTrack.id, SpotifyTrack.artist_id, TrackLyrics.id, TrackLyrics.language, *audio_features_columns, *artist_columns).\
            where(SpotifyTrack.id == AudioFeaturesDB.id).\
            where(SpotifyTrack.id == TrackLyrics.id).\
            where(SpotifyTrack.artist_id == SpotifyArtist.id).\
            limit(3)
        res = await execute_query(engine=self._db_engine, query=query)
        data = [Song.from_row(row) for row in res.all()]
        print('b')


if __name__ == "__main__":
    db_engine = get_database_engine()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(DatabaseClient(db_engine).query())
