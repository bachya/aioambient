"""Define tests for the REST API."""
import datetime

import aiohttp
import pytest

from aioambient import Client
from aioambient.errors import RequestError

from .common import TEST_API_KEY, TEST_APP_KEY, TEST_MAC, load_fixture


@pytest.mark.asyncio
async def test_api_error(aresponses):
    """Test the REST API raising an exception upon HTTP error."""
    aresponses.add(
        "dash2.ambientweather.net",
        "/v1/devices",
        "get",
        aresponses.Response(text="", status=500),
    )

    async with aiohttp.ClientSession() as websession:
        client = Client(TEST_API_KEY, TEST_APP_KEY, websession)

        with pytest.raises(RequestError):
            await client.api.get_devices()


@pytest.mark.asyncio
async def test_get_device_details(aresponses):
    """Test retrieving device details from the REST API."""
    aresponses.add(
        "dash2.ambientweather.net",
        f"/v1/devices/{TEST_MAC}",
        "get",
        aresponses.Response(
            text=load_fixture("device_details_response.json"), status=200
        ),
    )

    async with aiohttp.ClientSession() as websession:
        client = Client(TEST_API_KEY, TEST_APP_KEY, websession)

        device_details = await client.api.get_device_details(
            TEST_MAC, end_date=datetime.datetime(2019, 1, 6)
        )
        assert len(device_details) == 2


@pytest.mark.asyncio
async def test_get_devices(aresponses):
    """Test retrieving devices from the REST API."""
    aresponses.add(
        "dash2.ambientweather.net",
        "/v1/devices",
        "get",
        aresponses.Response(text=load_fixture("devices_response.json"), status=200),
    )

    async with aiohttp.ClientSession() as websession:
        client = Client(TEST_API_KEY, TEST_APP_KEY, websession)

        devices = await client.api.get_devices()
        assert len(devices) == 2
