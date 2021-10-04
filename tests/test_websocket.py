"""Define tests for the Websocket API."""
# pylint: disable=protected-access
import logging

import pytest
from socketio.exceptions import SocketIOError

from aioambient import Websocket
from aioambient.errors import WebsocketError
from aioambient.websocket import WebsocketWatchdog

from tests.async_mock import AsyncMock, MagicMock
from tests.common import TEST_API_KEY, TEST_APP_KEY


@pytest.mark.asyncio
async def test_connect_async_success():
    """Test connecting to the socket with an async handler."""
    websocket = Websocket(TEST_API_KEY, TEST_APP_KEY)
    websocket._sio.connect = AsyncMock()
    websocket._sio.eio._trigger_event = AsyncMock()
    websocket._sio.namespaces = {"/": 1}

    async_on_connect = AsyncMock()
    websocket.async_on_connect(async_on_connect)

    await websocket.connect()
    websocket._sio.connect.assert_called_once_with(
        f"https://api.ambientweather.net/?api=1&applicationKey={TEST_APP_KEY}",
        transports=["websocket"],
    )

    await websocket._sio._trigger_event("connect", "/")
    async_on_connect.assert_called_once()


@pytest.mark.asyncio
async def test_connect_sync_success():
    """Test connecting to the socket with a sync handler."""
    websocket = Websocket(TEST_API_KEY, TEST_APP_KEY)
    websocket._sio.connect = AsyncMock()
    websocket._sio.eio._trigger_event = AsyncMock()
    websocket._sio.namespaces = {"/": 1}

    async_on_connect = AsyncMock()
    websocket.async_on_connect(async_on_connect)

    await websocket.connect()
    websocket._sio.connect.assert_called_once_with(
        f"https://api.ambientweather.net/?api=1&applicationKey={TEST_APP_KEY}",
        transports=["websocket"],
    )

    await websocket._sio._trigger_event("connect", "/")
    async_on_connect.assert_called_once()


@pytest.mark.asyncio
async def test_connect_failure():
    """Test connecting to the socket and an exception occurring."""
    websocket = Websocket(TEST_API_KEY, TEST_APP_KEY)
    websocket._sio.connect = AsyncMock(side_effect=SocketIOError())

    with pytest.raises(WebsocketError):
        await websocket.connect()


@pytest.mark.asyncio
async def test_data_async():
    """Test data and subscription with async handlers."""
    websocket = Websocket(TEST_API_KEY, TEST_APP_KEY)
    websocket._sio.connect = AsyncMock()
    websocket._sio.disconnect = AsyncMock()
    websocket._sio.eio._trigger_event = AsyncMock()
    websocket._sio.namespaces = {"/": 1}

    async_on_connect = AsyncMock()
    async_on_data = AsyncMock()
    async_on_disconnect = AsyncMock()
    async_on_subscribed = AsyncMock()

    websocket.async_on_connect(async_on_connect)
    websocket.async_on_data(async_on_data)
    websocket.async_on_disconnect(async_on_disconnect)
    websocket.async_on_subscribed(async_on_subscribed)

    await websocket.connect()
    websocket._sio.connect.assert_called_once_with(
        f"https://api.ambientweather.net/?api=1&applicationKey={TEST_APP_KEY}",
        transports=["websocket"],
    )

    await websocket._sio._trigger_event("connect", "/")
    async_on_connect.assert_called_once()

    await websocket._sio._trigger_event("data", "/", {"foo": "bar"})
    async_on_data.assert_called_once()

    await websocket._sio._trigger_event("subscribed", "/", {"foo": "bar"})
    async_on_subscribed.assert_called()

    await websocket.disconnect()
    await websocket._sio._trigger_event("disconnect", "/")
    async_on_disconnect.assert_called_once()
    websocket._sio.disconnect.assert_called_once()


@pytest.mark.asyncio
async def test_data_sync():
    """Test data and subscription with sync handlers."""
    websocket = Websocket(TEST_API_KEY, TEST_APP_KEY)
    websocket._sio.connect = AsyncMock()
    websocket._sio.disconnect = AsyncMock()
    websocket._sio.eio._trigger_event = AsyncMock()
    websocket._sio.namespaces = {"/": 1}

    on_connect = MagicMock()
    on_data = MagicMock()
    on_disconnect = MagicMock()
    on_subscribed = MagicMock()

    websocket.on_connect(on_connect)
    websocket.on_data(on_data)
    websocket.on_disconnect(on_disconnect)
    websocket.on_subscribed(on_subscribed)

    await websocket.connect()
    websocket._sio.connect.assert_called_once_with(
        f"https://api.ambientweather.net/?api=1&applicationKey={TEST_APP_KEY}",
        transports=["websocket"],
    )

    await websocket._sio._trigger_event("connect", "/")
    on_connect.assert_called_once()

    await websocket._sio._trigger_event("data", "/", {"foo": "bar"})
    on_data.assert_called_once()

    await websocket._sio._trigger_event("subscribed", "/", {"foo": "bar"})
    on_subscribed.assert_called()

    await websocket.disconnect()
    await websocket._sio._trigger_event("disconnect", "/")
    on_disconnect.assert_called_once()
    websocket._sio.disconnect.assert_called_once()


@pytest.mark.asyncio
async def test_reconnect():
    """Test that reconnecting to the websocket does the right thing."""
    websocket = Websocket(TEST_API_KEY, TEST_APP_KEY)
    websocket._sio.connect = AsyncMock()
    websocket._sio.eio._trigger_event = AsyncMock()
    websocket._sio.namespaces = {"/": 1}

    async_on_connect = AsyncMock()
    async_on_disconnect = AsyncMock()

    websocket.async_on_connect(async_on_connect)
    websocket.async_on_disconnect(async_on_disconnect)

    await websocket.reconnect()
    await websocket._sio._trigger_event("disconnect", "/")
    async_on_disconnect.assert_called_once()
    await websocket._sio._trigger_event("connect", "/")
    async_on_connect.assert_called_once()


@pytest.mark.asyncio
async def test_watchdog_firing():
    """Test that the watchdog expiring fires the provided coroutine."""
    mock_coro = AsyncMock()
    mock_coro.__name__ = "mock_coro"

    watchdog = WebsocketWatchdog(logging.getLogger(), mock_coro)

    await watchdog.on_expire()
    mock_coro.assert_called_once()
