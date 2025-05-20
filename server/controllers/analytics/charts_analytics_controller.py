from typing import Dict, List

from genie_datastores.postgres.models import Chart, ChartEntry, SpotifyTrack, SpotifyArtist
from genie_datastores.postgres.operations import execute_query
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncEngine


class ChartsAnalyticsController:
    def __init__(self, db_engine: AsyncEngine) -> None:
        self._db_engine = db_engine

    async def get_chart_top_artists(self, chart: Chart, limit: int) -> List[Dict[str, str]]:
        query = (
            select(SpotifyArtist.id, SpotifyArtist.name, func.count().label("tracks_count"))
            .where(ChartEntry.track_id == SpotifyTrack.id)
            .where(SpotifyTrack.artist_id == SpotifyArtist.id)
            .where(ChartEntry.chart == chart)
            .group_by(SpotifyArtist.id, SpotifyArtist.name)
            .order_by(desc("tracks_count"))
            .limit(limit)
        )
        query_result = await execute_query(self._db_engine, query)
        result = query_result.all()

        return [{"artist": row.name, "count": row.tracks_count} for row in result]

    async def get_chart_top_tracks(self, chart: Chart, limit: int) -> List[Dict[str, str]]:
        query = (
            select(
                SpotifyTrack.id,
                SpotifyTrack.name,
                SpotifyArtist.name.label("artist_name"),
                func.count().label("tracks_count")
            )
            .where(ChartEntry.track_id == SpotifyTrack.id)
            .where(SpotifyTrack.artist_id == SpotifyArtist.id)
            .where(ChartEntry.chart == chart)
            .group_by(SpotifyTrack.id, SpotifyTrack.name, SpotifyArtist.name)
            .order_by(desc("tracks_count"))
            .limit(limit)
        )
        query_result = await execute_query(self._db_engine, query)
        result = query_result.all()

        return [{"artist": row.artist_name, "track": row.name, "count": row.tracks_count} for row in result]
