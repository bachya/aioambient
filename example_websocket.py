"""Run an example script to quickly test."""
import asyncio
import logging

from aioambient import Client
from aioambient.errors import WebsocketConnectionError, WebsocketError

_LOGGER = logging.getLogger()


def print_data(data):
    """Print data as it is received."""
    _LOGGER.info('Data received: %s', data)


def print_goodbye():
    """Print a simple "goodbye" message."""
    _LOGGER.info('Client has disconnected from the websocket')


def print_hello():
    """Print a simple "hello" message."""
    _LOGGER.info('Client has connected to the websocket')


async def main() -> None:
    """Run the websocket example."""
    logging.basicConfig(level=logging.INFO)

    # Create a client:
    client = Client('<YOUR API KEY>', '<YOUR APPLICATION KEY>')

    client.websocket.on_connect(print_hello)
    client.websocket.on_data(print_data)
    client.websocket.on_disconnect(print_goodbye)
    client.websocket.on_subscribed(print_data)

    try:
        await client.websocket.connect()
    except WebsocketConnectionError as err:
        _LOGGER.error('There was a websocket connection error: %s', err)
        return
    except WebsocketError as err:
        _LOGGER.error('There was a generic websocket error: %s', err)
        return

    for _ in range(30):
        _LOGGER.info('Simulating some other task occurring...')
        await asyncio.sleep(5)

    await client.websocket.disconnect()


loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()
