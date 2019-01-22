"""Run an example script to quickly test."""
import asyncio
import logging

from aiohttp import ClientSession

from aioambient import Client
from aioambient.errors import WebsocketConnectionError, WebsocketError

_LOGGER = logging.getLogger()

API_KEY = '<YOUR API KEY>'
APP_KEY = '<YOUR APPLICATION KEY>'


def print_data(data):
    """Print data as it is received."""
    print('Data received: ', data)


def print_goodbye():
    """Print a simple "goodbye" message."""
    print('Client has disconnected from the websocket')


def print_hello():
    """Print a simple "hello" message."""
    print('Client has connected to the websocket')


async def main() -> None:
    """Run the websocket example."""
    # logging.basicConfig(level=logging.INFO)

    async with ClientSession() as session:
        # Create a client:
        client = Client(API_KEY, APP_KEY, session)

        client.websocket.on_connect(print_hello)
        client.websocket.on_data(print_data)
        client.websocket.on_disconnect(print_goodbye)
        client.websocket.on_subscribed(print_data)

        try:
            await client.websocket.connect()
        except WebsocketConnectionError as err:
            print('There was a websocket connection error: {0}'.format(err))
            return
        except WebsocketError as err:
            print('There was a generic websocket error: {0}'.format(err))
            return

        for _ in range(30):
            print('Simulating some other task occurring...')
            await asyncio.sleep(5)

        await client.websocket.disconnect()


loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()
