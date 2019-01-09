"""Run an example script to quickly test."""
import asyncio
import logging

import socketio
from aiohttp import ClientSession

from aioambient import Client
from aioambient.errors import AmbientError

_LOGGER = logging.getLogger()

API_KEY = '12345'
APP_KEY = '12345'


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.DEBUG)
    async with ClientSession() as websession:
        try:
            # Create a client:
            client = Client(API_KEY, APP_KEY, websession)

            # Get all devices:
            devices = await client.devices.all()
            _LOGGER.info('Devices: %s', devices)

            # Wait 1 second to avoid rate limiting between calls:
            # https://ambientweather.docs.apiary.io/#introduction/rate-limiting
            await asyncio.sleep(1)

            # Get info on a specific device (by MAC address):
            details = await client.devices.details('84:F3:EB:21:90:C4')
            _LOGGER.info('Devices: %s', details)

            # sio = socketio.AsyncClient()
            # await sio.connect(
            #     'https://dash2.ambientweather.net?api=1&applicationKey={0}'.
            #     format(APP_KEY))
            # await sio.emit('subscribe', {'apiKeys': [API_KEY]})
            # await sio.wait()

        except AmbientError as err:
            print(err)


asyncio.get_event_loop().run_until_complete(main())
