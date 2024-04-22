from dataclasses import dataclass
from typing import Dict, List, Union

from aioresponses import aioresponses
from genie_datastores.postgres.models import PlaylistEndpoint

from server.data.case_status import CaseStatus
from tests.server.integration.test_resources import TestResources


@dataclass
class PlaylistControllerTestContext:
    case_id: str
    endpoint: PlaylistEndpoint
    expected_progress_statuses: List[CaseStatus]
    mock_responses: aioresponses
    payload: Dict[str, Union[str, dict]]
    playlist_id: str
    resources: TestResources
    uris: List[str]
