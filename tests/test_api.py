"""Define tests for the REST API."""
import datetime
import json

import aiohttp
import pytest

from aioambient import Client
from aioambient.errors import RequestError

from .const import TEST_API_KEY, TEST_APP_KEY, TEST_MAC
from .fixtures.api import device_details_json, devices_json


@pytest.mark.asyncio
async def test_api_error(aresponses, devices_json):
    """Test an API error occurring."""
    aresponses.add(
        "api.ambientweather.net",
        "/v1/devices",
        "get",
        aresponses.Response(text="", status=500),
    )

    client = Client(TEST_API_KEY, TEST_APP_KEY)

    with pytest.raises(RequestError):
        await client.api.get_devices()


@pytest.mark.asyncio
async def test_get_device_details(aresponses, device_details_json):
    """Test geting details on a device."""
    aresponses.add(
        "api.ambientweather.net",
        "/v1/devices/{0}".format(TEST_MAC),
        "get",
        aresponses.Response(text=json.dumps(device_details_json), status=200),
    )

    client = Client(TEST_API_KEY, TEST_APP_KEY)

    device_details = await client.api.get_device_details(
        TEST_MAC, end_date=datetime.datetime(2019, 1, 6))
    assert len(device_details) == 2


@pytest.mark.asyncio
async def test_get_devices(aresponses, devices_json):
    """Test geting all devices from an account."""
    aresponses.add(
        "api.ambientweather.net",
        "/v1/devices",
        "get",
        aresponses.Response(text=json.dumps(devices_json), status=200),
    )

    client = Client(TEST_API_KEY, TEST_APP_KEY)

    devices = await client.api.get_devices()
    assert len(devices) == 2
