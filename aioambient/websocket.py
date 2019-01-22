"""Define an object to interact with the Websocket API."""
from typing import Awaitable, Callable, Union

from socketio import AsyncClient
from socketio.exceptions import ConnectionError, SocketIOError

from .errors import WebsocketConnectionError, WebsocketError

WEBSOCKET_API_BASE = 'https://dash2.ambientweather.net'


class Websocket:
    """Define to handler."""

    def __init__(
            self, application_key: str, api_key: str,
            api_version: int) -> None:
        """Initialize."""
        self._api_key = api_key
        self._api_version = api_version
        self._application_key = application_key
        self._sio = AsyncClient()

    def on_connect(self, target: Union[Awaitable, Callable]) -> None:
        """Define a method/coroutine to be called when connecting."""
        self._sio.on('connect', target)

    def on_data(self, target: Union[Awaitable, Callable]) -> None:
        """Define a method/coroutine to be called when data is received."""
        self._sio.on('data', target)

    def on_disconnect(self, target: Union[Awaitable, Callable]) -> None:
        """Define a method/coroutine to be called when disconnecting."""
        self._sio.on('disconnect', target)

    def on_subscribed(self, target: Union[Awaitable, Callable]) -> None:
        """Define a method/coroutine to be called when subscribed."""
        self._sio.on('subscribed', target)

    async def connect(self) -> None:
        """Connect to the socket."""
        try:
            await self._sio.connect(
                '{0}/?api={1}&applicationKey={2}'.format(
                    WEBSOCKET_API_BASE, self._api_version,
                    self._application_key),
                transports=['websocket'])
        except (ConnectionError, SocketIOError) as err:
            raise WebsocketConnectionError(err) from None

        try:
            await self._sio.emit('subscribe', {'apiKeys': [self._api_key]})
        except (ConnectionError, SocketIOError) as err:
            raise WebsocketError(err) from None

    async def disconnect(self) -> None:
        """Disconnect from the socket."""
        await self._sio.disconnect()
