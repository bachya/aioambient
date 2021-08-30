"""Define an object to interact with the REST API."""
import asyncio
from datetime import date
import logging
from typing import Any, Dict, List, Optional, cast

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError

from .errors import RequestError

REST_API_BASE: str = "https://api.ambientweather.net"

DEFAULT_LIMIT: int = 288
DEFAULT_TIMEOUT: int = 10


class API:
    """Define the API object."""

    def __init__(
        self,
        logger: logging.Logger,
        application_key: str,
        api_key: str,
        api_version: int,
        *,
        session: Optional[ClientSession] = None,
    ) -> None:
        """Initialize."""
        self._api_key: str = api_key
        self._api_version: int = api_version
        self._application_key: str = application_key
        self._logger = logger
        self._session: Optional[ClientSession] = session

    async def _request(
        self, method: str, endpoint: str, **kwargs: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Make a request against the API."""
        # In order to deal with Ambient's fairly aggressive rate limiting, we
        # pause for a second before continuing in case any requests came before
        # this.
        # https://ambientweather.docs.apiary.io/#introduction/rate-limiting
        await asyncio.sleep(1)

        url = f"{REST_API_BASE}/v{self._api_version}/{endpoint}"

        kwargs.setdefault("params", {})
        kwargs["params"]["apiKey"] = self._api_key
        kwargs["params"]["applicationKey"] = self._application_key

        use_running_session = self._session and not self._session.closed

        if use_running_session:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))

        assert session

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

        return cast(List[Dict[str, Any]], data)

    async def get_devices(self) -> List[Dict[str, Any]]:
        """Get all devices associated with an API key."""
        return await self._request("get", "devices")

    async def get_device_details(
        self,
        mac_address: str,
        *,
        end_date: Optional[date] = None,
        limit: int = DEFAULT_LIMIT,
    ) -> list:
        """Get details of a device by MAC address."""
        params: Dict[str, Any] = {"limit": limit}
        if end_date:
            params["endDate"] = end_date.isoformat()

        return await self._request("get", f"devices/{mac_address}", params=params)
