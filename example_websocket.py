"""Run an example script to quickly test."""
import asyncio
import logging

from aiohttp import ClientSession

from aioambient import Client

_LOGGER = logging.getLogger()

API_KEY = '486b9ac473f34e6ba73af698a0e01f262c42ac73a1e343e990147dad7d6c7e5f'
APP_KEY = '32f561c4cb3a400d9c71ae0e96495466beaea220e315403c955b8f2bb12ac9a1'


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
        await client.websocket.connect()

        for _ in range(30):
            print('Simulating some other task occurring...')
            await asyncio.sleep(5)

        await client.websocket.disconnect()


loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()
