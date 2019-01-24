"""Define tests for the Websocket API."""
import aiohttp
import pytest
from unittest.mock import patch, MagicMock

from socketio.exceptions import SocketIOError

from aioambient import Client
from aioambient.errors import WebsocketConnectionError, WebsocketError

from tests.const import TEST_API_KEY, TEST_APP_KEY


def async_mock(*args, **kwargs):
    """Return a mock asynchronous function."""
    m = MagicMock(*args, **kwargs)

    async def mock_coro(*args, **kwargs):
        return m(*args, **kwargs)

    mock_coro.mock = m
    return mock_coro


@pytest.mark.asyncio
async def test_connect_success():
    """Test connecting to the socket."""
    client = Client(TEST_API_KEY, TEST_APP_KEY)
    client.websocket._sio.eio.connect = async_mock()

    await client.websocket.connect()
    client.websocket._sio.eio.connect.mock.assert_called_once_with(
        'https://dash2.ambientweather.net/?api=1&applicationKey={0}'.
        format(TEST_APP_KEY),
        engineio_path='socket.io',
        headers={},
        transports=['websocket'])


@pytest.mark.asyncio
async def test_connect_failure():
    """Test connecting to the socket and an exception occurring."""
    client = Client(TEST_API_KEY, TEST_APP_KEY)
    client.websocket._sio.eio.connect = async_mock(
        side_effect=SocketIOError())

    with pytest.raises(WebsocketConnectionError):
        await client.websocket.connect()


@pytest.mark.asyncio
async def test_general_failure():
    """Test a generic exception occurring."""
    client = Client(TEST_API_KEY, TEST_APP_KEY)
    client.websocket._sio._send_packet = async_mock(
        side_effect=SocketIOError())
    client.websocket._sio.eio.connect = async_mock()

    with pytest.raises(WebsocketError):
        await client.websocket.connect()
        await client.websocket._sio.emit('test')


@pytest.mark.asyncio
async def test_events():
    """Test all events and handlers."""
    client = Client(TEST_API_KEY, TEST_APP_KEY)
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
    await client.websocket._sio._trigger_event('disconnect', '/')
    on_subscribed.assert_called_once()
    client.websocket._sio.eio.disconnect.mock.assert_called_once_with(
        abort=True)
