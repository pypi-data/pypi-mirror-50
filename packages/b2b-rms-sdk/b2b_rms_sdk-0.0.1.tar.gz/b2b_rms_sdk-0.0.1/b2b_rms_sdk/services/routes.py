from http import HTTPStatus
from typing import List

import requests

from b2b_rms_sdk.models import B2BRoute


class B2BRouteService:
    def __init__(self, b2b_rms_url):
        self._url = b2b_rms_url

    def get_by_names(self, names: List) -> B2BRoute:
        response = requests.get(
            f"{self._url}/api/v1/routes/by_names", json={"names": names}
        )

        if response != HTTPStatus.OK:
            raise _mk_err(response)

        return B2BRoute.from_dict(response.json().get("data"))

    def get_hydrated_route(self, route_id) -> B2BRoute:
        route_res = requests.get(f"{self._url}/api/v1/routes/{route_id}")
        route_path_res = requests.get(f"{self._url}/api/v1/routes/{route_id}/path")
        route_departures_res = requests.get(
            f"{self._url}/api/v1/routes/{route_id}/stop_times"
        )

        if not route_res.status_code == HTTPStatus.OK:
            raise _mk_err(route_res)

        if not route_path_res.status_code == HTTPStatus.OK:
            raise _mk_err(route_path_res)

        if not route_departures_res.status_code == HTTPStatus.OK:
            raise _mk_err(route_departures_res)

        route = route_res.json()["data"]
        route_path = route_path_res.json()["data"]
        route_departures = route_departures_res.json()["data"]

        return B2BRoute.from_dict(route, route_path, route_departures)


def _mk_err(response):
    err_msg = f"""
    B2B RMS Failure

    Status Code: {response.status_code} 
    Response: {response.text} 
    """
    return RuntimeError(err_msg)


def get_b2b_route_service(b2b_rms_url: str):
    return B2BRouteService(b2b_rms_url)
