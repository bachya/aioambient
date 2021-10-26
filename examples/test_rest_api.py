"""Run an example script to quickly test."""
import asyncio
import logging

from aiohttp import ClientSession

from aioambient import API
from aioambient.errors import AmbientError

_LOGGER = logging.getLogger()

API_KEY = "<YOUR API KEY>"
APP_KEY = "<YOUR APPLICATION KEY>"


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)
    async with ClientSession() as session:
        try:
            api = API(APP_KEY, API_KEY, session=session)

            devices = await api.get_devices()
            _LOGGER.info("Devices: %s", devices)

            for device in devices:
                details = await api.get_device_details(device["macAddress"])
                _LOGGER.info("Device Details (%s): %s", device["macAddress"], details)

        except AmbientError as err:
            _LOGGER.error("There was an error: %s", err)


asyncio.run(main())
