"""Define an object to interact with the REST API."""
from __future__ import annotations

import asyncio
import logging
from typing import Any, cast

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError

from .const import LOGGER
from .errors import RequestError

DEFAULT_TIMEOUT = 10


class ApiRequestHandler:  # pylint: disable=too-few-public-methods
    """Handle API requests. Base class for both the API and OpenAPI classes.
    Handles all requests to Ambient services."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        base_url: str,
        *,
        logger: logging.Logger = LOGGER,
        session: ClientSession | None = None,
    ) -> None:
        """Initialize.

        Args:
            base_url: Base URL for each request
            logger: The logger to use.
            session: An optional aiohttp ClientSession.
        """
        self._logger = logger
        self._session: ClientSession | None = session
        self._base_url = base_url

    async def _request(
        self, method: str, endpoint: str, **kwargs: dict[str, Any]
    ) -> list[dict[str, Any]] | dict[str, Any]:
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

        url = f"{self._base_url}/{endpoint}"

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

        # Returns either a list of dicts or a dict itself.
        return cast(list[dict[str, Any]] | dict[str, Any], data)
