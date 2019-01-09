"""Run an example script to quickly test."""
import asyncio
import logging

import socketio
from aiohttp import ClientSession

from aioambient import Client
from aioambient.errors import AmbientError

_LOGGER = logging.getLogger()

API_KEY = '<YOUR API KEY>'
APP_KEY = '<YOUR API KEY>'


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)
    async with ClientSession() as websession:
        try:
            # Create a client:
            client = Client(API_KEY, APP_KEY, websession)

            # Get all devices:
            devices = await client.api.get_devices()
            _LOGGER.info('Devices: %s', devices)

            # Wait 1 second to avoid rate limiting between calls:
            # https://ambientweather.docs.apiary.io/#introduction/rate-limiting
            await asyncio.sleep(1)

            # Get info on a specific device (by MAC address):
            details = await client.api.get_device_details('84:F3:EB:21:90:C4')
            _LOGGER.info('Devices: %s', details)
        except AmbientError as err:
            _LOGGER.error('There was an error: %s', err)
    # sio = socketio.AsyncClient()

    # @sio.on('connect')
    # async def on_connect():
    #     _LOGGER.info('Websocket connected')

    # await sio.connect(
    #     'https://dash2.ambientweather.net?api=1&applicationKey={0}'.format(
    #         APP_KEY),
    #     transports=['websocket'])
    # await sio.emit('subscribe', {'apiKeys': [API_KEY]})
    # await sio.wait()


asyncio.get_event_loop().run_until_complete(main())
