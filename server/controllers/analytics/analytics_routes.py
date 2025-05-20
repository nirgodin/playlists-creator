from typing import Annotated

from fastapi import APIRouter, Depends
from genie_datastores.postgres.models import Chart
from starlette.responses import JSONResponse

from server.component_factory import get_charts_analytics_controller
from server.controllers.analytics.charts_analytics_controller import ChartsAnalyticsController

analytics_router = APIRouter(prefix='/analytics', tags=['analytics'])


@analytics_router.get("/charts/top_artists")
async def get_chart_top_artists(
        charts_analytics_controller: Annotated[ChartsAnalyticsController, Depends(get_charts_analytics_controller)],
        chart: Chart,
        limit: int = 5
) -> JSONResponse:
    content = await charts_analytics_controller.get_chart_top_artists(chart, limit)
    return JSONResponse(content=content)


@analytics_router.get("/charts/top_tracks")
async def get_chart_top_artists(
        charts_analytics_controller: Annotated[ChartsAnalyticsController, Depends(get_charts_analytics_controller)],
        chart: Chart,
        limit: int = 5
) -> JSONResponse:
    content = await charts_analytics_controller.get_chart_top_tracks(chart, limit)
    return JSONResponse(content=content)
