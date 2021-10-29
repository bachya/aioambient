"""Define tests for the REST API."""
import datetime
import logging

import aiohttp
import pytest

from aioambient import API
from aioambient.errors import RequestError

from .common import TEST_API_KEY, TEST_APP_KEY, TEST_MAC, load_fixture


@pytest.mark.asyncio
async def test_api_error(aresponses):
    """Test the REST API raising an exception upon HTTP error."""
    aresponses.add(
        "rt.ambientweather.net",
        "/v1/devices",
        "get",
        aresponses.Response(text="", status=500),
    )

    async with aiohttp.ClientSession() as session:
        api = API(TEST_API_KEY, TEST_APP_KEY, session=session)

        with pytest.raises(RequestError):
            await api.get_devices()


@pytest.mark.asyncio
async def test_custom_logger(aresponses, caplog):
    """Test that a custom logger is used when provided to the client."""
    caplog.set_level(logging.DEBUG)
    custom_logger = logging.getLogger("custom")

    aresponses.add(
        "rt.ambientweather.net",
        f"/v1/devices/{TEST_MAC}",
        "get",
        aresponses.Response(
            text=load_fixture("device_details_response.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        api = API(TEST_API_KEY, TEST_APP_KEY, session=session, logger=custom_logger)

        await api.get_device_details(TEST_MAC, end_date=datetime.date(2019, 1, 6))
        assert any(
            record.name == "custom" and "Received data" in record.message
            for record in caplog.records
        )


@pytest.mark.asyncio
async def test_get_device_details(aresponses):
    """Test retrieving device details from the REST API."""
    aresponses.add(
        "rt.ambientweather.net",
        f"/v1/devices/{TEST_MAC}",
        "get",
        aresponses.Response(
            text=load_fixture("device_details_response.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        api = API(TEST_API_KEY, TEST_APP_KEY, session=session)

        device_details = await api.get_device_details(
            TEST_MAC, end_date=datetime.date(2019, 1, 6)
        )
        assert len(device_details) == 2


@pytest.mark.asyncio
async def test_get_devices(aresponses):
    """Test retrieving devices from the REST API."""
    aresponses.add(
        "rt.ambientweather.net",
        "/v1/devices",
        "get",
        aresponses.Response(
            text=load_fixture("devices_response.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        api = API(TEST_API_KEY, TEST_APP_KEY, session=session)

        devices = await api.get_devices()
        assert len(devices) == 2


@pytest.mark.asyncio
async def test_session_from_scratch(aresponses):
    """Test that an aiohttp ClientSession is created on the fly if needed."""
    aresponses.add(
        "rt.ambientweather.net",
        "/v1/devices",
        "get",
        aresponses.Response(
            text=load_fixture("devices_response.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    api = API(TEST_API_KEY, TEST_APP_KEY)

    devices = await api.get_devices()
    assert len(devices) == 2
