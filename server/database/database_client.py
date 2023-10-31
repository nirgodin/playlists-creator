import asyncio

import pandas as pd
from postgres_client.models.orm.audio_features import AudioFeatures as AudioFeaturesDB
from postgres_client.models.orm.spotify_artist import SpotifyArtist
from postgres_client.models.orm.spotify_track import SpotifyTrack
from postgres_client.models.orm.track_lyrics import TrackLyrics
from postgres_client.postgres_operations import execute_query, get_database_engine
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine

from server.consts.database_consts import ARTIST_COLUMNS, AUDIO_FEATURES_COLUMNS, TRACK_COLUMNS
from server.database.database_models.track import Track


class DatabaseClient:
    def __init__(self, db_engine: AsyncEngine):
        self._db_engine = db_engine

    async def query(self):
        query = select(*TRACK_COLUMNS, TrackLyrics.language, *AUDIO_FEATURES_COLUMNS, *ARTIST_COLUMNS).\
            where(SpotifyTrack.id == AudioFeaturesDB.id).\
            where(SpotifyTrack.id == TrackLyrics.id).\
            where(SpotifyTrack.artist_id == SpotifyArtist.id).\
            where(AudioFeaturesDB.key == 11).\
            limit(5)

        res = await execute_query(engine=self._db_engine, query=query)
        data = pd.DataFrame.from_records([Track.from_row(row).to_record() for row in res.all()])
        print('b')


if __name__ == "__main__":
    db_engine = get_database_engine()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(DatabaseClient(db_engine).query())
