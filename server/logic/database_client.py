from functools import lru_cache
from typing import List, Tuple

from genie_common.tools import logger
from genie_datastores.postgres.models import RadioTrack, SpotifyTrack, AudioFeatures, TrackLyrics, SpotifyArtist, Artist
from genie_datastores.postgres.operations import execute_query
from genie_datastores.postgres.utils import get_orm_columns
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.sql import Subquery, Select
from sqlalchemy.sql.elements import TextClause

from server.consts.database_consts import RADIO_TRACK_COLUMNS
from server.data.query_condition import QueryCondition
from server.tools.case_progress_reporter import CaseProgressReporter


# TODO: Maybe not belong here, but remove tracks that are not available on any market as they cannot be played
class DatabaseClient:
    def __init__(self, db_engine: AsyncEngine, case_progress_reporter: CaseProgressReporter):
        self._db_engine = db_engine
        self._case_progress_reporter = case_progress_reporter

    async def query(self, case_id: str, query_conditions: List[QueryCondition]) -> List[str]:
        logger.info("Starting to query database for relevant tracks ids")

        async with self._case_progress_reporter.report(case_id=case_id, status="tracks"):
            query = self._build_query(query_conditions)
            query_result = await execute_query(engine=self._db_engine, query=query)
            tracks_ids = query_result.scalars().all()

        logger.info(f"Successfully queried database and found `{len(tracks_ids)}` relevant tracks")
        return tracks_ids

    def _build_query(self, query_conditions: List[QueryCondition]) -> Select:
        spotify_conditions, radio_conditions = self._split_conditions(query_conditions)
        spotify_subquery = self._build_spotify_subquery(spotify_conditions)
        radio_subquery = self._build_radio_subquery(spotify_subquery, radio_conditions)

        return select(radio_subquery.c.track_id)

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
            .where(SpotifyArtist.id == Artist.id)
            .where(*conditions)
        )

        return spotify_subquery.subquery("spotify")

    def _build_radio_subquery(self, spotify_subquery: Subquery, radio_conditions: List[QueryCondition]):
        conditions = self._serialize_conditions(radio_conditions)
        radio_subquery = (
            select(*RADIO_TRACK_COLUMNS)
            .where(RadioTrack.track_id.in_(spotify_subquery))
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
