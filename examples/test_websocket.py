"""Run an example script to quickly test."""
import asyncio
import logging

from aiohttp import ClientSession

from aioambient import Client
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


async def main() -> None:
    """Run the websocket example."""
    logging.basicConfig(level=logging.INFO)

    async with ClientSession() as session:
        client = Client(API_KEY, APP_KEY, session)

        client.websocket.on_connect(print_hello)
        client.websocket.on_data(print_data)
        client.websocket.on_disconnect(print_goodbye)
        client.websocket.on_subscribed(print_data)

        try:
            await client.websocket.connect()
        except WebsocketError as err:
            _LOGGER.error("There was a websocket error: %s", err)
            return

        while True:
            _LOGGER.info("Simulating some other task occurring...")
            await asyncio.sleep(5)


loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()
