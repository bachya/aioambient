"""Define tests for the REST API."""
import re

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from aioambient import OpenAPI

from .common import TEST_MAC, load_fixture


@pytest.mark.asyncio
async def test_get_device_details(aresponses: ResponsesMockServer) -> None:
    """Test retrieving device details from the open REST API.

    Args:
        aresponses: An aresponses server.
    """
    aresponses.add(
        "lightning.ambientweather.net",
        f"/devices/{TEST_MAC}",
        "get",
        aresponses.Response(
            text=load_fixture("device_details_open_response.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        api = OpenAPI(session=session)

        device_details = await api.get_device_details(TEST_MAC)
        assert "lastData" in device_details


@pytest.mark.asyncio
async def test_get_devices_by_location(aresponses: ResponsesMockServer) -> None:
    """Test retrieving devices from the open REST API.

    Args:
        aresponses: An aresponses server.
    """
    aresponses.add(
        "lightning.ambientweather.net",
        re.compile(r"/devices.*"),
        "get",
        aresponses.Response(
            text=load_fixture("devices_by_location_open_response.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        api = OpenAPI(session=session)

        devices = await api.get_devices_by_location(32.5, -97.3, 1.5)
        assert len(devices) == 6
