"""Define an object to interact with the Websocket API."""
import asyncio
import logging
from typing import Any, Awaitable, Callable, Dict, List, Optional, Union

from aiohttp.client_exceptions import ClientConnectionError, ClientOSError
from socketio import AsyncClient
from socketio.exceptions import ConnectionError as SIOConnectionError, SocketIOError

from .const import DEFAULT_API_VERSION, LOGGER
from .errors import WebsocketError

DEFAULT_WATCHDOG_TIMEOUT = 900

WEBSOCKET_API_BASE = "https://rt2.ambientweather.net"


class WebsocketWatchdog:
    """Define a watchdog to kick the websocket connection at intervals."""

    def __init__(
        self,
        logger: logging.Logger,
        action: Callable[..., Awaitable],
        *,
        timeout_seconds: int = DEFAULT_WATCHDOG_TIMEOUT,
    ):
        """Initialize."""
        self._action = action
        self._logger = logger
        self._loop = asyncio.get_event_loop()
        self._timeout = timeout_seconds
        self._timer_task: Optional[asyncio.TimerHandle] = None

    def cancel(self) -> None:
        """Cancel the watchdog."""
        if self._timer_task:
            self._timer_task.cancel()
            self._timer_task = None

    async def on_expire(self) -> None:
        """Log and act when the watchdog expires."""
        self._logger.info("Watchdog expired – calling %s", self._action.__name__)
        await self._action()

    async def trigger(self) -> None:
        """Trigger the watchdog."""
        self._logger.info("Watchdog triggered – sleeping for %s seconds", self._timeout)

        if self._timer_task:
            self._timer_task.cancel()

        self._timer_task = self._loop.call_later(
            self._timeout, lambda: asyncio.create_task(self.on_expire())
        )


class Websocket:  # pylint: disable=too-many-instance-attributes
    """Define the websocket."""

    def __init__(
        self,
        application_key: str,
        api_key: Union[List[str], str],
        *,
        api_version: int = DEFAULT_API_VERSION,
        logger: logging.Logger = LOGGER,
    ) -> None:
        """Initialize."""
        if isinstance(api_key, str):
            api_key = [api_key]

        self._api_key = api_key
        self._api_version = api_version
        self._app_key = application_key
        self._async_user_connect_handler: Optional[Callable[..., Awaitable]] = None
        self._logger = logger
        self._sio = AsyncClient(logger=logger, engineio_logger=logger)
        self._user_connect_handler: Optional[Callable] = None
        self._watchdog = WebsocketWatchdog(logger, self.reconnect)

    async def _init_connection(self) -> None:
        """Perform automatic initialization upon connecting."""
        await self._sio.emit("subscribe", {"apiKeys": self._api_key})
        await self._watchdog.trigger()

        if self._async_user_connect_handler:
            await self._async_user_connect_handler()
        elif self._user_connect_handler:
            self._user_connect_handler()

    def async_on_connect(self, target: Callable[..., Awaitable]) -> None:
        """Define a coroutine to be called when connecting."""
        self._async_user_connect_handler = target
        self._user_connect_handler = None

    def on_connect(self, target: Callable) -> None:
        """Define a method to be called when connecting."""
        self._async_user_connect_handler = None
        self._user_connect_handler = target

    def async_on_data(self, target: Callable[..., Awaitable]) -> None:  # noqa: D202
        """Define a coroutine to be called when data is received."""

        async def _async_on_data(data: Dict[str, Any]) -> None:
            """Act on the data."""
            await self._watchdog.trigger()
            await target(data)

        self._sio.on("data", _async_on_data)

    def on_data(self, target: Callable) -> None:  # noqa: D202
        """Define a method to be called when data is received."""

        async def _async_on_data(data: Dict[str, Any]) -> None:
            """Act on the data."""
            await self._watchdog.trigger()
            target(data)

        self._sio.on("data", _async_on_data)

    def async_on_disconnect(self, target: Callable[..., Awaitable]) -> None:
        """Define a coroutine to be called when disconnecting."""
        self._sio.on("disconnect", target)

    def on_disconnect(self, target: Callable) -> None:
        """Define a method to be called when disconnecting."""
        self._sio.on("disconnect", target)

    def async_on_subscribed(
        self, target: Callable[..., Awaitable]
    ) -> None:  # noqa: D202
        """Define a coroutine to be called when subscribed."""

        async def _async_on_subscribed(data: Dict[str, Any]) -> None:
            """Act on subscribe."""
            await self._watchdog.trigger()
            await target(data)

        self._sio.on("subscribed", _async_on_subscribed)

    def on_subscribed(self, target: Callable) -> None:  # noqa: D202
        """Define a method to be called when subscribed."""

        async def _async_on_subscribed(data: Dict[str, Any]) -> None:
            """Act on subscribe."""
            await self._watchdog.trigger()
            target(data)

        self._sio.on("subscribed", _async_on_subscribed)

    async def connect(self) -> None:
        """Connect to the socket."""
        try:
            self._sio.on("connect", self._init_connection)
            await self._sio.connect(
                f"{WEBSOCKET_API_BASE}/?api={self._api_version}&applicationKey={self._app_key}",
                transports=["websocket"],
            )
        except (
            ClientConnectionError,
            ClientOSError,
            SIOConnectionError,
            SocketIOError,
        ) as err:
            raise WebsocketError(err) from err

    async def disconnect(self) -> None:
        """Disconnect from the socket."""
        await self._sio.disconnect()
        self._watchdog.cancel()

    async def reconnect(self) -> None:
        """Reconnect the websocket connection."""
        await self.disconnect()
        await asyncio.sleep(1)
        await self.connect()
