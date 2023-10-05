"""Define an object to interact with the REST API."""
from __future__ import annotations

import asyncio
import logging
from datetime import date
from typing import Any, cast

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError

from .const import DEFAULT_API_VERSION, LOGGER
from .errors import RequestError

REST_API_BASE = "https://rt.ambientweather.net"

DEFAULT_LIMIT = 288
DEFAULT_TIMEOUT = 10


class API:
    """Define the API object."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        application_key: str,
        api_key: str,
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
        self._api_key: str = api_key
        self._api_version: int = api_version
        self._application_key: str = application_key
        self._logger = logger
        self._session: ClientSession | None = session

    async def _request(
        self, method: str, endpoint: str, **kwargs: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Make a request against the API.

        In order to deal with Ambient's fairly aggressive rate limiting, we
        pause for a second before continuing:
        https://ambientweather.docs.apiary.io/#introduction/rate-limiting

        Args:
            method: An HTTP method.
            endpoint: A relative API endpoint.
            **kwargs: Additional kwargs to send with the request.

        Returns:
            An API response payload.

        Raises:
            RequestError: Raised upon an underlying HTTP error.
        """
        await asyncio.sleep(1)

        url = f"{REST_API_BASE}/v{self._api_version}/{endpoint}"

        kwargs.setdefault("params", {})
        kwargs["params"]["apiKey"] = self._api_key
        kwargs["params"]["applicationKey"] = self._application_key

        if use_running_session := self._session and not self._session.closed:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))

        try:
            async with session.request(method, url, **kwargs) as resp:
                resp.raise_for_status()
                data = await resp.json()
        except ClientError as err:
            raise RequestError(f"Error requesting data from {url}: {err}") from err
        finally:
            if not use_running_session:
                await session.close()

        self._logger.debug("Received data for %s: %s", endpoint, data)

        return cast(list[dict[str, Any]], data)

    async def get_devices(self) -> list[dict[str, Any]]:
        """Get all devices associated with an API key.

        Returns:
            An API response payload.
        """
        return await self._request("get", "devices")

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
        params: dict[str, Any] = {"limit": limit}
        if end_date:
            params["endDate"] = end_date.isoformat()

        return await self._request("get", f"devices/{mac_address}", params=params)
