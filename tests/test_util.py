"""Define tests for utilities."""

import pytest

from aioambient.util import get_public_device_id
from aioambient.util.location_utils import LocationUtils


@pytest.mark.asyncio
async def test_get_public_id() -> None:
    """Test getting the public ID of a device by its MAC address."""
    public_id = get_public_device_id("AB:CD:EF:12:34:56")
    assert public_id == "04629a94fef5bfb62b525a6784cb8b37"


@pytest.mark.asyncio
async def test_shift_location() -> None:
    """Test for shift_location utility function."""
    lat, long = LocationUtils.shift_location(0, 0, 1, 1)
    assert lat == 0.014472285807800538
    assert long == 0.014472285807800538

    lat, long = LocationUtils.shift_location(40, 30, 1, 1)
    assert lat == 40.014472285807805
    assert long == 30.018892227386804

    lat, long = LocationUtils.shift_location(80, 20, -5, -5)
    assert lat == 79.927638570961
    assert long == 19.5832871383321
