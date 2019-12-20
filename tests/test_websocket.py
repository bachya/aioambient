"""Define tests for the Websocket API."""
from unittest.mock import MagicMock, patch

import aiohttp
import pytest
from socketio.exceptions import SocketIOError

from aioambient import Client
from aioambient.errors import WebsocketError

from tests.const import TEST_API_KEY, TEST_APP_KEY


def async_mock(*args, **kwargs):
    """Return a mock asynchronous function."""
    m = MagicMock(*args, **kwargs)

    async def mock_coro(*args, **kwargs):
        return m(*args, **kwargs)

    mock_coro.mock = m
    return mock_coro


async def test_connect_async_success(event_loop):
    """Test connecting to the socket with an async handler."""
    async with aiohttp.ClientSession(loop=event_loop) as session:
        client = Client(TEST_API_KEY, TEST_APP_KEY, session)
        client.websocket._sio.eio._trigger_event = async_mock()
        client.websocket._sio.eio.connect = async_mock()

        on_connect = async_mock()
        client.websocket.async_on_connect(on_connect)

        await client.websocket.connect()
        client.websocket._sio.eio.connect.mock.assert_called_once_with(
            f"https://dash2.ambientweather.net/?api=1&applicationKey={TEST_APP_KEY}",
            engineio_path="socket.io",
            headers={},
            transports=["websocket"],
        )

        await client.websocket._sio._trigger_event("connect", namespace="/")
        on_connect.mock.assert_called_once()


async def test_connect_sync_success(event_loop):
    """Test connecting to the socket with a sync handler."""
    async with aiohttp.ClientSession(loop=event_loop) as session:
        client = Client(TEST_API_KEY, TEST_APP_KEY, session)
        client.websocket._sio.eio._trigger_event = async_mock()
        client.websocket._sio.eio.connect = async_mock()

        on_connect = MagicMock()
        client.websocket.on_connect(on_connect)

        await client.websocket.connect()
        client.websocket._sio.eio.connect.mock.assert_called_once_with(
            f"https://dash2.ambientweather.net/?api=1&applicationKey={TEST_APP_KEY}",
            engineio_path="socket.io",
            headers={},
            transports=["websocket"],
        )

        await client.websocket._sio._trigger_event("connect", namespace="/")
        on_connect.assert_called_once()


async def test_connect_failure(event_loop):
    """Test connecting to the socket and an exception occurring."""
    async with aiohttp.ClientSession(loop=event_loop) as session:
        client = Client(TEST_API_KEY, TEST_APP_KEY, session)
        client.websocket._sio.eio.connect = async_mock(side_effect=SocketIOError())

        with pytest.raises(WebsocketError):
            await client.websocket.connect()


async def async_test_events(event_loop):
    """Test all events and async_handlers."""
    async with aiohttp.ClientSession(loop=event_loop) as session:
        client = Client(TEST_API_KEY, TEST_APP_KEY, session)
        client.websocket._sio.eio._trigger_event = async_mock()
        client.websocket._sio.eio.connect = async_mock()
        client.websocket._sio.eio.disconnect = async_mock()

        on_connect = MagicMock()
        on_data = MagicMock()
        on_subscribed = MagicMock()

        client.websocket.on_connect(on_connect)
        client.websocket.on_data(on_data)
        client.websocket.on_disconnect(on_data)
        client.websocket.on_subscribed(on_subscribed)

        await client.websocket.connect()
        client.websocket._sio.eio.connect.mock.assert_called_once_with(
            f"https://dash2.ambientweather.net/?api=1&applicationKey={TEST_APP_KEY}",
            engineio_path="socket.io",
            headers={},
            transports=["websocket"],
        )

        await client.websocket._sio._trigger_event("connect", namespace="/")
        on_connect.assert_called_once()

        await client.websocket._sio._trigger_event("data", namespace="/")
        on_data.assert_called_once()

        await client.websocket._sio._trigger_event("subscribed", namespace="/")
        on_subscribed.assert_called()

        await client.websocket.disconnect()
        await client.websocket._sio._trigger_event("disconnect", namespace="/")
        on_subscribed.assert_called_once()
        client.websocket._sio.eio.disconnect.mock.assert_called_once_with(abort=True)


async def test_events(event_loop):
    """Test all events and handlers."""
    async with aiohttp.ClientSession(loop=event_loop) as session:
        client = Client(TEST_API_KEY, TEST_APP_KEY, session)
        client.websocket._sio.eio._trigger_event = async_mock()
        client.websocket._sio.eio.connect = async_mock()
        client.websocket._sio.eio.disconnect = async_mock()

        on_connect = async_mock()
        on_data = async_mock()
        on_subscribed = async_mock()

        client.websocket.async_on_connect(on_connect)
        client.websocket.async_on_data(on_data)
        client.websocket.async_on_disconnect(on_data)
        client.websocket.async_on_subscribed(on_subscribed)

        await client.websocket.connect()
        client.websocket._sio.eio.connect.mock.assert_called_once_with(
            f"https://dash2.ambientweather.net/?api=1&applicationKey={TEST_APP_KEY}",
            engineio_path="socket.io",
            headers={},
            transports=["websocket"],
        )

        await client.websocket._sio._trigger_event("connect", namespace="/")
        on_connect.mock.assert_called_once()

        await client.websocket._sio._trigger_event("data", namespace="/")
        on_data.mock.assert_called_once()

        await client.websocket._sio._trigger_event("subscribed", namespace="/")
        on_subscribed.mock.assert_called()

        await client.websocket.disconnect()
        await client.websocket._sio._trigger_event("disconnect", namespace="/")
        on_subscribed.mock.assert_called_once()
        client.websocket._sio.eio.disconnect.mock.assert_called_once_with(abort=True)
