"""Define tests for the Websocket API."""
import aiohttp
import pytest
from unittest.mock import patch, MagicMock

from aioambient import Client

from tests.const import TEST_API_KEY, TEST_APP_KEY


def async_mock(*args, **kwargs):
    """Return a mock asynchronous function."""
    m = MagicMock(*args, **kwargs)

    async def mock_coro(*args, **kwargs):
        return m(*args, **kwargs)

    mock_coro.mock = m
    return mock_coro


@pytest.mark.asyncio
async def test_connect(event_loop):
    """Test connecting to the socket."""
    async with aiohttp.ClientSession(loop=event_loop) as session:
        client = Client(TEST_API_KEY, TEST_APP_KEY, session)
        client.websocket._sio.eio.connect = async_mock()

        await client.websocket.connect()
        client.websocket._sio.eio.connect.mock.assert_called_once_with(
            'https://dash2.ambientweather.net/?api=1&applicationKey={0}'.
            format(TEST_APP_KEY),
            engineio_path='socket.io',
            headers={},
            transports=['websocket'])


@pytest.mark.asyncio
async def test_handlers(event_loop):
    """Test all handlers."""
    async with aiohttp.ClientSession(loop=event_loop) as session:
        client = Client(TEST_API_KEY, TEST_APP_KEY, session)
        client.websocket._sio.eio._trigger_event = async_mock()
        client.websocket._sio.eio.connect = async_mock()
        client.websocket._sio.eio.disconnect = async_mock()

        on_connect = MagicMock()
        on_data = MagicMock()
        on_disconnect = MagicMock()
        on_subscribed = MagicMock()

        client.websocket.on_connect(on_connect)
        client.websocket.on_data(on_data)
        client.websocket.on_disconnect(on_data)
        client.websocket.on_subscribed(on_subscribed)

        await client.websocket.connect()
        client.websocket._sio.eio.connect.mock.assert_called_once_with(
            'https://dash2.ambientweather.net/?api=1&applicationKey={0}'.
            format(TEST_APP_KEY),
            engineio_path='socket.io',
            headers={},
            transports=['websocket'])

        await client.websocket._sio._trigger_event('connect', '/', 'my_arg')
        on_connect.assert_called_once_with('my_arg')

        await client.websocket._sio._trigger_event('data', '/', 'my_arg')
        on_data.assert_called_once_with('my_arg')

        await client.websocket._sio._trigger_event('subscribed', '/', 'my_arg')
        on_subscribed.assert_called_once_with('my_arg')

        await client.websocket.disconnect()
        await client.websocket._sio._trigger_event('discoonecft', '/')
        on_subscribed.assert_called_once()
        client.websocket._sio.eio.disconnect.mock.assert_called_once_with(
            abort=True)
