"""Define an object to interact with the REST API."""
import asyncio
from datetime import datetime
from typing import Any, Dict

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError

from .errors import RequestError

REST_API_BASE: str = "https://dash2.ambientweather.net"
DEFAULT_LIMIT: int = 288


class API:
    """Define the API object."""

    def __init__(
        self,
        application_key: str,
        api_key: str,
        api_version: int,
        session: ClientSession,
    ) -> None:
        """Initialize."""
        self._api_key: str = api_key
        self._api_version: int = api_version
        self._application_key: str = application_key
        self._session: ClientSession = session

    async def _request(
        self, method: str, endpoint: str, *, params: dict = None
    ) -> list:
        """Make a request against the API."""
        # In order to deal with Ambient's fairly aggressive rate limiting, we
        # pause for a second before continuing in case any requests came before
        # this.
        # https://ambientweather.docs.apiary.io/#introduction/rate-limiting
        await asyncio.sleep(1)

        url: str = f"{REST_API_BASE}/v{self._api_version}/{endpoint}"

        if not params:
            params = {}
        params.update(
            {"apiKey": self._api_key, "applicationKey": self._application_key}
        )

        async with self._session.request(method, url, params=params) as resp:
            try:
                resp.raise_for_status()
                return await resp.json(content_type=None)
            except ClientError as err:
                raise RequestError(f"Error requesting data from {url}: {err}")

    async def get_devices(self) -> list:
        """Get all devices associated with an API key."""
        return await self._request("get", "devices")

    async def get_device_details(
        self, mac_address: str, *, end_date: datetime = None, limit: int = DEFAULT_LIMIT
    ) -> list:
        """Get details of a device by MAC address."""
        params: Dict[str, Any] = {"limit": limit}
        if end_date:
            params["endDate"] = end_date.isoformat()

        return await self._request("get", f"devices/{mac_address}", params=params)
