import asyncio
from functools import lru_cache
from typing import List, Tuple

from postgres_client import execute_query, get_orm_columns, RadioTrack, SpotifyTrack, AudioFeatures, TrackLyrics, \
    SpotifyArtist, get_database_engine
from sqlalchemy import select, Subquery, TextClause
from sqlalchemy.ext.asyncio import AsyncEngine

from server.consts.database_consts import RADIO_TRACK_COLUMNS
from server.data.query_condition import QueryCondition


class DatabaseClient:
    def __init__(self, db_engine: AsyncEngine):
        self._db_engine = db_engine

    async def query(self, query_conditions: List[QueryCondition]) -> List[str]:
        spotify_conditions, radio_conditions = self._split_conditions(query_conditions)
        spotify_subquery = self._build_spotify_subquery(spotify_conditions)
        radio_subquery = self._build_radio_subquery(spotify_subquery, radio_conditions)
        query = select(radio_subquery.c.track_id)
        query_result = await execute_query(engine=self._db_engine, query=query)

        return query_result.scalars().all()

    def _split_conditions(self, conditions: List[QueryCondition]) -> Tuple[List[QueryCondition], List[QueryCondition]]:
        radio_conditions = []
        radio_columns = self._get_radio_track_column_names()

        for i, condition in enumerate(conditions):
            if condition.column in radio_columns:
                radio_condition = conditions.pop(i)
                radio_conditions.append(radio_condition)

        return conditions, radio_conditions

    @staticmethod
    @lru_cache
    def _get_radio_track_column_names() -> List[str]:
        return [col.name for col in get_orm_columns(RadioTrack)]

    def _build_spotify_subquery(self, spotify_conditions: List[QueryCondition]):
        conditions = self._serialize_conditions(spotify_conditions)
        spotify_subquery = (
            select(SpotifyTrack.id)
            .where(SpotifyTrack.id == AudioFeatures.id)
            .where(SpotifyTrack.id == TrackLyrics.id)
            .where(SpotifyTrack.artist_id == SpotifyArtist.id)
            .where(*conditions)
        )

        return spotify_subquery.subquery("spotify")

    def _build_radio_subquery(self, spotify_subquery: Subquery, radio_conditions: List[QueryCondition]):
        conditions = self._serialize_conditions(radio_conditions)
        radio_subquery = (
            select(*RADIO_TRACK_COLUMNS)
            .where(RadioTrack.track_id.in_(spotify_subquery))
            .where(RadioTrack.popularity > 56)
            .where(*conditions)
            .group_by(RadioTrack.track_id)
        )

        return radio_subquery.subquery("radio")

    @staticmethod
    def _serialize_conditions(conditions: List[QueryCondition]) -> List[TextClause]:
        text_clauses = []

        for condition in conditions:
            if condition.condition is not None:
                text_clauses.append(condition.condition)

        return text_clauses


if __name__ == "__main__":
    db_engine = get_database_engine()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(DatabaseClient(db_engine).query(
        [QueryCondition("popularity", ">", 50), QueryCondition("valence", "<", 0.8)]
    )
    )
