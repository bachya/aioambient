"""Run an example script to quickly test."""
import asyncio
import logging

from aioambient import Websocket
from aioambient.errors import WebsocketError

_LOGGER = logging.getLogger()

API_KEY = "<YOUR API KEY>"
APP_KEY = "<YOUR APPLICATION KEY>"


def print_data(data):
    """Print data as it is received."""
    _LOGGER.info("Data received: %s", data)


def print_goodbye():
    """Print a simple "goodbye" message."""
    _LOGGER.info("Client has disconnected from the websocket")


def print_hello():
    """Print a simple "hello" message."""
    _LOGGER.info("Client has connected to the websocket")


def print_subscribed(data):
    """Print subscription data as it is received."""
    _LOGGER.info("Client has subscribed: %s", data)


async def main() -> None:
    """Run the websocket example."""
    logging.basicConfig(level=logging.INFO)

    websocket = Websocket(APP_KEY, API_KEY)

    websocket.on_connect(print_hello)
    websocket.on_data(print_data)
    websocket.on_disconnect(print_goodbye)
    websocket.on_subscribed(print_subscribed)

    try:
        await websocket.connect()
    except WebsocketError as err:
        _LOGGER.error("There was a websocket error: %s", err)
        return

    while True:
        _LOGGER.info("Simulating some other task occurring...")
        await asyncio.sleep(5)


loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()
