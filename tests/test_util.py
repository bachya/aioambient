"""Define tests for utilities."""
import pytest

from aioambient.util import get_public_device_id


@pytest.mark.asyncio
async def test_get_public_id() -> None:
    """Test getting the public ID of a device by its MAC address."""
    public_id = get_public_device_id("AB:CD:EF:12:34:56")
    assert public_id == "04629a94fef5bfb62b525a6784cb8b37"
