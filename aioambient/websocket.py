"""Define an object to interact with the Websocket API."""
from typing import Awaitable, Callable, Optional, Union

from socketio import AsyncClient
from socketio.exceptions import (  # pylint: disable=redefined-builtin
    ConnectionError,
    SocketIOError,
)

from .errors import WebsocketError

WEBSOCKET_API_BASE: str = "https://dash2.ambientweather.net"


class Websocket:
    """Define the websocket."""

    def __init__(self, application_key: str, api_key: str, api_version: int) -> None:
        """Initialize."""
        self._api_key: str = api_key
        self._api_version: int = api_version
        self._app_key: str = application_key
        self._async_user_connect_handler: Optional[Awaitable] = None
        self._sio: AsyncClient = AsyncClient()
        self._user_connect_handler: Optional[Callable] = None

    async def _init_connection(self) -> None:
        """Perform automatic initialization upon connecting."""
        await self._sio.emit("subscribe", {"apiKeys": [self._api_key]})

        if self._async_user_connect_handler:
            await self._async_user_connect_handler()  # type: ignore
        elif self._user_connect_handler:
            self._user_connect_handler()

    def async_on_connect(self, target: Awaitable) -> None:
        """Define a coroutine to be called when connecting."""
        self._async_user_connect_handler = target
        self._user_connect_handler = None

    def on_connect(self, target: Callable) -> None:
        """Define a method to be called when connecting."""
        self._async_user_connect_handler = None
        self._user_connect_handler = target

    def async_on_data(self, target: Awaitable) -> None:
        """Define a coroutine to be called when data is received."""
        self.on_data(target)

    def on_data(self, target: Union[Awaitable, Callable]) -> None:
        """Define a method to be called when data is received."""
        self._sio.on("data", target)

    def async_on_disconnect(self, target: Awaitable) -> None:
        """Define a coroutine to be called when disconnecting."""
        self.on_disconnect(target)

    def on_disconnect(self, target: Union[Awaitable, Callable]) -> None:
        """Define a method to be called when disconnecting."""
        self._sio.on("disconnect", target)

    def async_on_subscribed(self, target: Awaitable) -> None:
        """Define a coroutine to be called when subscribed."""
        self.on_subscribed(target)

    def on_subscribed(self, target: Union[Awaitable, Callable]) -> None:
        """Define a method to be called when subscribed."""
        self._sio.on("subscribed", target)

    async def connect(self) -> None:
        """Connect to the socket."""
        try:
            self._sio.on("connect", self._init_connection)
            await self._sio.connect(
                f"{WEBSOCKET_API_BASE}/?api={self._api_version}&applicationKey={self._app_key}",
                transports=["websocket"],
            )
        except (ConnectionError, SocketIOError) as err:
            raise WebsocketError(err) from None

    async def disconnect(self) -> None:
        """Disconnect from the socket."""
        await self._sio.disconnect()
