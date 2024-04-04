from http import HTTPStatus
from typing import Dict, List, Tuple

from fastapi import FastAPI
from fastapi.routing import APIRoute
from genie_common.utils import random_alphanumeric_string, get_all_enum_values, contains_all_substrings
from genie_datastores.postgres.models import PlaylistEndpoint

from tests.server.integration.test_resources import TestResources


class TestAppAuthentication:
    async def test_unauthorized_request__returns_401(self, resources: TestResources):
        for url, method in self._get_api_paths_methods_map(resources.app):
            auth = (random_alphanumeric_string(), random_alphanumeric_string())

            response = resources.client.request(method=method, url=url, auth=auth)

            assert response.status_code == HTTPStatus.UNAUTHORIZED.value
            assert response.json() == {"message": "Unauthorized"}

    def _get_api_paths_methods_map(self, app: FastAPI) -> List[Tuple[str, str]]:
        paths_methods_map = []

        for route in app.routes:
            if isinstance(route, APIRoute):
                for method in route.methods:
                    for path in self._get_route_paths(route):
                        paths_methods_map.append((path, method))

        return paths_methods_map

    def _get_route_paths(self, route: APIRoute) -> List[str]:
        if self._has_path_parameters(route):
            return self._routes_format_routes_map[route.path]
        else:
            return [route.path]

    @staticmethod
    def _has_path_parameters(route: APIRoute) -> bool:
        return contains_all_substrings(route.path, ["{", "}"])

    @property
    def _routes_format_routes_map(self) -> Dict[str, List[str]]:
        endpoints = get_all_enum_values(PlaylistEndpoint)
        return {
            "/api/cases/{case_id}/progress": [f"/api/cases/{random_alphanumeric_string()}/progress"],
            "/api/cases/{case_id}/playlist": [f"/api/cases/{random_alphanumeric_string()}/playlist"],
            "/api/playlist/{endpoint}": [f"/api/playlist/{endpoint}" for endpoint in endpoints]
        }
