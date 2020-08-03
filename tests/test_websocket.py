"""Define tests for the Websocket API."""
# pylint: disable=protected-access
import aiohttp
from asynctest import CoroutineMock, MagicMock
import pytest
from socketio.exceptions import SocketIOError

from aioambient import Client
from aioambient.errors import WebsocketError
from aioambient.websocket import WebsocketWatchdog

from .common import TEST_API_KEY, TEST_APP_KEY


async def test_connect_async_success(event_loop):
    """Test connecting to the socket with an async handler."""
    async with aiohttp.ClientSession(loop=event_loop) as session:
        client = Client(TEST_API_KEY, TEST_APP_KEY, session=session)
        client.websocket._sio.eio._trigger_event = CoroutineMock()
        client.websocket._sio.eio.connect = CoroutineMock()

        async_on_connect = CoroutineMock()
        client.websocket.async_on_connect(async_on_connect)

        await client.websocket.connect()
        client.websocket._sio.eio.connect.assert_called_once_with(
            f"https://api.ambientweather.net/?api=1&applicationKey={TEST_APP_KEY}",
            engineio_path="socket.io",
            headers={},
            transports=["websocket"],
        )

        await client.websocket._sio._trigger_event("connect", "/")
        async_on_connect.assert_called_once()


async def test_connect_sync_success(event_loop):
    """Test connecting to the socket with a sync handler."""
    async with aiohttp.ClientSession(loop=event_loop) as session:
        client = Client(TEST_API_KEY, TEST_APP_KEY, session=session)
        client.websocket._sio.eio._trigger_event = CoroutineMock()
        client.websocket._sio.eio.connect = CoroutineMock()

        async_on_connect = CoroutineMock()
        client.websocket.async_on_connect(async_on_connect)

        await client.websocket.connect()
        client.websocket._sio.eio.connect.assert_called_once_with(
            f"https://api.ambientweather.net/?api=1&applicationKey={TEST_APP_KEY}",
            engineio_path="socket.io",
            headers={},
            transports=["websocket"],
        )

        await client.websocket._sio._trigger_event("connect", "/")
        async_on_connect.assert_called_once()


async def test_connect_failure(event_loop):
    """Test connecting to the socket and an exception occurring."""
    async with aiohttp.ClientSession(loop=event_loop) as session:
        client = Client(TEST_API_KEY, TEST_APP_KEY, session=session)
        client.websocket._sio.eio.connect = CoroutineMock(side_effect=SocketIOError())

        with pytest.raises(WebsocketError):
            await client.websocket.connect()


async def test_data_async(event_loop):
    """Test data and subscription with async handlers."""
    async with aiohttp.ClientSession(loop=event_loop) as session:
        client = Client(TEST_API_KEY, TEST_APP_KEY, session=session)
        client.websocket._sio.eio._trigger_event = CoroutineMock()
        client.websocket._sio.eio.connect = CoroutineMock()
        client.websocket._sio.eio.disconnect = CoroutineMock()

        async_on_connect = CoroutineMock()
        async_on_data = CoroutineMock()
        async_on_disconnect = CoroutineMock()
        async_on_subscribed = CoroutineMock()

        client.websocket.async_on_connect(async_on_connect)
        client.websocket.async_on_data(async_on_data)
        client.websocket.async_on_disconnect(async_on_disconnect)
        client.websocket.async_on_subscribed(async_on_subscribed)

        await client.websocket.connect()
        client.websocket._sio.eio.connect.assert_called_once_with(
            f"https://api.ambientweather.net/?api=1&applicationKey={TEST_APP_KEY}",
            engineio_path="socket.io",
            headers={},
            transports=["websocket"],
        )

        await client.websocket._sio._trigger_event("connect", "/")
        async_on_connect.assert_called_once()

        await client.websocket._sio._trigger_event("data", "/", {"foo": "bar"})
        async_on_data.assert_called_once()

        await client.websocket._sio._trigger_event("subscribed", "/", {"foo": "bar"})
        async_on_subscribed.assert_called()

        await client.websocket.disconnect()
        await client.websocket._sio._trigger_event("disconnect", "/")
        async_on_disconnect.assert_called_once()
        client.websocket._sio.eio.disconnect.assert_called_once_with(abort=True)


async def test_data_sync(event_loop):
    """Test data and subscription with sync handlers."""
    async with aiohttp.ClientSession(loop=event_loop) as session:
        client = Client(TEST_API_KEY, TEST_APP_KEY, session=session)
        client.websocket._sio.eio._trigger_event = CoroutineMock()
        client.websocket._sio.eio.connect = CoroutineMock()
        client.websocket._sio.eio.disconnect = CoroutineMock()

        on_connect = MagicMock()
        on_data = MagicMock()
        on_disconnect = MagicMock()
        on_subscribed = MagicMock()

        client.websocket.on_connect(on_connect)
        client.websocket.on_data(on_data)
        client.websocket.on_disconnect(on_disconnect)
        client.websocket.on_subscribed(on_subscribed)

        await client.websocket.connect()
        client.websocket._sio.eio.connect.assert_called_once_with(
            f"https://api.ambientweather.net/?api=1&applicationKey={TEST_APP_KEY}",
            engineio_path="socket.io",
            headers={},
            transports=["websocket"],
        )

        await client.websocket._sio._trigger_event("connect", "/")
        on_connect.assert_called_once()

        await client.websocket._sio._trigger_event("data", "/", {"foo": "bar"})
        on_data.assert_called_once()

        await client.websocket._sio._trigger_event("subscribed", "/", {"foo": "bar"})
        on_subscribed.assert_called()

        await client.websocket.disconnect()
        await client.websocket._sio._trigger_event("disconnect", "/")
        on_disconnect.assert_called_once()
        client.websocket._sio.eio.disconnect.assert_called_once_with(abort=True)


async def test_reconnect(event_loop):
    """Test that reconnecting to the websocket does the right thing."""
    async with aiohttp.ClientSession(loop=event_loop) as session:
        client = Client(TEST_API_KEY, TEST_APP_KEY, session=session)
        client.websocket._sio.eio._trigger_event = CoroutineMock()
        client.websocket._sio.eio.connect = CoroutineMock()

        async_on_connect = CoroutineMock()
        async_on_disconnect = CoroutineMock()

        client.websocket.async_on_connect(async_on_connect)
        client.websocket.async_on_disconnect(async_on_disconnect)

        await client.websocket.reconnect()
        await client.websocket._sio._trigger_event("disconnect", "/")
        async_on_disconnect.assert_called_once()
        await client.websocket._sio._trigger_event("connect", "/")
        async_on_connect.assert_called_once()


@pytest.mark.asyncio
async def test_watchdog_firing():
    """Test that the watchdog expiring fires the provided coroutine."""
    mock_coro = CoroutineMock()
    mock_coro.__name__ = "mock_coro"

    watchdog = WebsocketWatchdog(mock_coro)

    await watchdog.on_expire()
    mock_coro.assert_called_once()
