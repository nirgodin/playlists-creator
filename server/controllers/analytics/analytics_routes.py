from typing import Annotated, Callable, Dict, Coroutine, List, Any, Optional

from fastapi import APIRouter, Depends
from genie_datastores.models import EntityType
from genie_datastores.postgres.models import Chart
from starlette.responses import JSONResponse

from server.component_factory import get_charts_analytics_controller
from server.controllers.analytics.charts_analytics_controller import ChartsAnalyticsController

analytics_router = APIRouter(prefix='/analytics', tags=['analytics'])


@analytics_router.get("/charts/top/{entity_type}")
async def get_chart_top_entities(
        charts_analytics_controller: Annotated[ChartsAnalyticsController, Depends(get_charts_analytics_controller)],
        entity_type: EntityType,
        chart: Chart,
        limit: int = 5,
        position: Optional[int] = None,
) -> JSONResponse:
    entity_type_method_map: Dict[EntityType, Callable[[Chart, int, Optional[int]], Coroutine[Any, Any, list]]] = {
        EntityType.ARTIST: charts_analytics_controller.get_chart_top_artists,
        EntityType.TRACK: charts_analytics_controller.get_chart_top_tracks,
    }
    method = entity_type_method_map[entity_type]
    content = await method(
        chart,
        limit,
        position
    )

    return JSONResponse(content=content)
