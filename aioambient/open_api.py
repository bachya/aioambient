"""Define an object to interact with the open REST API."""
from __future__ import annotations

import logging
from typing import Any, cast

from aiohttp import ClientSession

from aioambient.api_request_handler import ApiRequestHandler
from aioambient.util.climate_utils import ClimateUtils
from aioambient.util.location_utils import LocationUtils

from .const import LOGGER

REST_API_BASE = "https://lightning.ambientweather.net"


class OpenAPI(ApiRequestHandler):
    """Define the OpenAPI object."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        *,
        logger: logging.Logger = LOGGER,
        session: ClientSession | None = None,
    ) -> None:
        """Initialize.

        Args:
            logger: The logger to use.
            session: An optional aiohttp ClientSession.
        """
        super().__init__(REST_API_BASE, logger=logger, session=session)

    @staticmethod
    def inject_virtual_values(data: dict[str, Any]) -> None:
        """Inject dew point and feels like temperature.

        The regular (private) API computes the "feels like" and the "dew point"
        temperature on the server-side and returns the values as part of the API
        response. The open API, on the other hand, calculates the two values on
        the client side and the two values are not part of the API response.
        The following code manually calculates the "feels like" and the "dew point"
        temperature to replicate the server-side logic of the private API.

        Arguments:
            data: Map of station data.
        """

        if (last_data := data.get("lastData")) is None:
            return

        if all(key in last_data for key in ("tempf", "humidity")):
            last_data["dewPoint"] = ClimateUtils.dew_point_fahrenheit(
                last_data["tempf"], last_data["humidity"]
            )

        if all(key in last_data for key in ("tempf", "humidity", "windspeedmph")):
            last_data["feelsLike"] = ClimateUtils.feels_like_fahrenheit(
                last_data["tempf"],
                last_data["humidity"],
                last_data["windspeedmph"],
            )

    async def get_devices_by_location(
        self, latitude: float, longitude: float, radius: float = 1.0
    ) -> list[dict[str, Any]]:
        """Get all devices registered within an area of `radius`
        miles from the center given by (`latitude`, `longitude`).

        Args:
            latitude: Latitude of center.
            longitude: Longigude of center.
            radius: Radius (in miles).

        Returns:
            An API response payload.
        """
        lat1, long1 = LocationUtils.shift_location(
            latitude, longitude, -radius, -radius
        )
        lat2, long2 = LocationUtils.shift_location(
            latitude, longitude, +radius, +radius
        )
        params = {}
        params["$publicBox[0][0]"] = long1
        params["$publicBox[0][1]"] = lat1
        params["$publicBox[1][0]"] = long2
        params["$publicBox[1][1]"] = lat2
        params["$limit"] = 100

        # This endpoint returns a dict with a single "data" field that contains
        # a list of device dicts.
        response = cast(
            dict[str, Any], await self._request("get", "devices", params=params)
        )
        if (response_data := response.get("data")) is not None:
            for station_data in response_data:
                OpenAPI.inject_virtual_values(station_data)
        return cast(list[dict[str, Any]], response_data)

    async def get_device_details(self, mac_address: str) -> dict[str, Any]:
        """Get details of a device by MAC address.

        Args:
            mac_address: The MAC address of an Ambient Weather station.

        Returns:
            An API response payload.
        """
        # This endpoint returns a single data dict.
        response = cast(
            dict[str, Any], await self._request("get", f"devices/{mac_address}")
        )
        OpenAPI.inject_virtual_values(response)
        return response
