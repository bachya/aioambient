"""Define package utilities."""
import math
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


def shift_location(
    latitude: float, longitude: float, latitude_delta: float, longitude_delta: float
) -> tuple[float, float]:
    """Calculates a new (latitude, longitude) pair by shifting the location
    given by (`latitude`, `longitude`) by (`latitude_delta`, `longitude_delta`).

    Args:
        latitude: Latitude (in degrees).
        longitude: Longitude (in degrees).
        latitude_delta: Latitude delta (in miles).
        longitude_delta: Longitude delta (in miles).

    Returns:
        New (latitude, longitude) pair.
    """

    # Radius of the Earth in miles
    earth_radius = 3959.0

    # Convert latitude and longitude from degrees to radians
    latitude_rad = math.radians(latitude)
    longitude_rad = math.radians(longitude)

    # Calculate angular distance in radians
    angular_latitude_delta = latitude_delta / earth_radius
    angular_longitude_delta = longitude_delta / earth_radius

    # Calculate new latitude
    new_latitude_rad = latitude_rad + angular_latitude_delta

    # Calculate new longitude
    new_longitude_rad = longitude_rad + angular_longitude_delta / math.cos(latitude_rad)

    # Convert new latitude and longitude from radians to degrees
    new_latitude = math.degrees(new_latitude_rad)
    new_longitude = math.degrees(new_longitude_rad)

    return new_latitude, new_longitude
