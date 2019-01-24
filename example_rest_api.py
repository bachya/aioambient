"""Run an example script to quickly test."""
import asyncio
import logging

from aioambient import Client
from aioambient.errors import AmbientError

_LOGGER = logging.getLogger()


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)

    try:
        # Create a client:
        client = Client('<YOUR API KEY>', '<YOUR APPLICATION KEY>')

        # Get all devices:
        devices = await client.api.get_devices()
        _LOGGER.info('Devices: %s', devices)

        for device in devices:
            # Get info on a specific device (by MAC address):
            details = await client.api.get_device_details(
                device['macAddress'])
            _LOGGER.info(
                'Device Details (%s): %s', device['macAddress'], details)

    except AmbientError as err:
        _LOGGER.error('There was an error: %s', err)


asyncio.get_event_loop().run_until_complete(main())
