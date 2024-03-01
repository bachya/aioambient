"""Define an object to interact with the REST API."""

from __future__ import annotations

import logging
from datetime import date
from typing import Any, cast

from aiohttp import ClientSession

from .api_request_handler import ApiRequestHandler
from .const import DEFAULT_API_VERSION, LOGGER

REST_API_BASE = "https://rt.ambientweather.net"

DEFAULT_LIMIT = 288


class API(ApiRequestHandler):
    """Define the API object."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        application_key: str | None,
        api_key: str | None,
        *,
        api_version: int = DEFAULT_API_VERSION,
        logger: logging.Logger = LOGGER,
        session: ClientSession | None = None,
    ) -> None:
        """Initialize.

        Args:
            application_key: An Ambient Weather application key.
            api_key: An Ambient Weather API key.
            api_version: The version of the API to query.
            logger: The logger to use.
            session: An optional aiohttp ClientSession.
        """
        super().__init__(
            f"{REST_API_BASE}/v{api_version}", logger=logger, session=session
        )
        self._api_key = api_key
        self._application_key = application_key

    async def get_devices(self) -> list[dict[str, Any]]:
        """Get all devices associated with an API key.

        Returns:
            An API response payload.
        """
        params: dict[str, Any] = {
            "apiKey": self._api_key,
            "applicationKey": self._application_key,
        }

        # This endpoint returns a list of device dicts.
        return cast(
            list[dict[str, Any]], await self._request("get", "devices", params=params)
        )

    async def get_device_details(
        self,
        mac_address: str,
        *,
        end_date: date | None = None,
        limit: int = DEFAULT_LIMIT,
    ) -> list[dict[str, Any]]:
        """Get details of a device by MAC address.

        Args:
            mac_address: The MAC address of an Ambient Weather station.
            end_date: An optional end date to limit data.
            limit: An optional limit.

        Returns:
            An API response payload.
        """
        params: dict[str, Any] = {
            "apiKey": self._api_key,
            "applicationKey": self._application_key,
            "limit": limit,
        }
        if end_date:
            params["endDate"] = end_date.isoformat()

        # This endpoint returns a list device data dicts.
        return cast(
            list[dict[str, Any]],
            await self._request("get", f"devices/{mac_address}", params=params),
        )
