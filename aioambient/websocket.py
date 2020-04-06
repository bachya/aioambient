"""Define an object to interact with the Websocket API."""
import asyncio
import logging
from typing import Awaitable, Callable, Optional

from aiohttp.client_exceptions import ClientConnectionError, ClientOSError
from socketio import AsyncClient
from socketio.exceptions import (  # pylint: disable=redefined-builtin
    ConnectionError,
    SocketIOError,
)

from .errors import WebsocketError

_LOGGER = logging.getLogger(__name__)

DEFAULT_WATCHDOG_TIMEOUT = 900

WEBSOCKET_API_BASE: str = "https://dash2.ambientweather.net"


class WebsocketWatchdog:
    """Define a watchdog to kick the websocket connection at intervals."""

    def __init__(
        self,
        action: Callable[..., Awaitable],
        *,
        timeout_seconds: int = DEFAULT_WATCHDOG_TIMEOUT,
    ):
        """Initialize."""
        self._action: Callable[..., Awaitable] = action
        self._loop = asyncio.get_event_loop()
        self._timer_task: Optional[asyncio.TimerHandle] = None
        self._timeout: int = timeout_seconds

    def cancel(self):
        """Cancel the watchdog."""
        if self._timer_task:
            self._timer_task.cancel()
            self._timer_task = None

    async def on_expire(self):
        """Log and act when the watchdog expires."""
        _LOGGER.info("Watchdog expired – calling %s", self._action.__name__)
        await self._action()

    async def trigger(self):
        """Trigger the watchdog."""
        _LOGGER.info("Watchdog triggered – sleeping for %s seconds", self._timeout)

        if self._timer_task:
            self._timer_task.cancel()

        self._timer_task = self._loop.call_later(
            self._timeout, lambda: asyncio.create_task(self.on_expire())
        )


class Websocket:
    """Define the websocket."""

    def __init__(self, application_key: str, api_key: str, api_version: int) -> None:
        """Initialize."""
        self._api_key: str = api_key
        self._api_version: int = api_version
        self._app_key: str = application_key
        self._async_user_connect_handler: Optional[Callable[..., Awaitable]] = None
        self._sio: AsyncClient = AsyncClient()
        self._user_connect_handler: Optional[Callable] = None
        self._watchdog: WebsocketWatchdog = WebsocketWatchdog(self.reconnect)

    async def _init_connection(self) -> None:
        """Perform automatic initialization upon connecting."""
        await self._sio.emit("subscribe", {"apiKeys": [self._api_key]})
        await self._watchdog.trigger()

        if self._async_user_connect_handler:
            await self._async_user_connect_handler()  # type: ignore
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

        async def _async_on_data(data: dict):
            """Act on the data."""
            await self._watchdog.trigger()
            await target(data)

        self._sio.on("data", _async_on_data)

    def on_data(self, target: Callable) -> None:  # noqa: D202
        """Define a method to be called when data is received."""

        async def _async_on_data(data: dict):
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

        async def _async_on_subscribed(data):
            """Act on subscribe."""
            await self._watchdog.trigger()
            await target(data)

        self._sio.on("subscribed", _async_on_subscribed)

    def on_subscribed(self, target: Callable) -> None:  # noqa: D202
        """Define a method to be called when subscribed."""

        async def _async_on_subscribed(data):
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
            ConnectionError,
            SocketIOError,
        ) as err:
            raise WebsocketError(err) from None

    async def disconnect(self) -> None:
        """Disconnect from the socket."""
        await self._sio.disconnect()
        self._watchdog.cancel()

    async def reconnect(self) -> None:
        """Reconnect the websocket connection."""
        await self.disconnect()
        await asyncio.sleep(1)
        await self.connect()
