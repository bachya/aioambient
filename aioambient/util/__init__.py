"""Define package utilities."""

from hashlib import md5


def get_public_device_id(mac_address: str) -> str:
    """Get the public device ID (if it exists) of a device by MAC address.

    Args:
        mac_address: The MAC address of the device.

    Returns:
        The public-facing device ID.
    """
    public_id = mac_address
    for _ in range(2):
        public_id = md5(public_id.encode("utf-8"), usedforsecurity=False).hexdigest()
    return public_id
