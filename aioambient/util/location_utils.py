"""Location utility functions."""

import math

# Radius of the Earth in miles
EARTH_RADIUS = 3959.0


class LocationUtils:  # pylint: disable=too-few-public-methods
    """Location utility functions."""

    @staticmethod
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

        # Convert latitude and longitude from degrees to radians
        latitude_rad = math.radians(latitude)
        longitude_rad = math.radians(longitude)

        # Calculate angular distance in radians
        angular_latitude_delta = latitude_delta / EARTH_RADIUS
        angular_longitude_delta = longitude_delta / EARTH_RADIUS

        # Calculate new latitude
        new_latitude_rad = latitude_rad + angular_latitude_delta

        # Calculate new longitude
        new_longitude_rad = longitude_rad + angular_longitude_delta / math.cos(
            latitude_rad
        )

        # Convert new latitude and longitude from radians to degrees
        new_latitude = math.degrees(new_latitude_rad)
        new_longitude = math.degrees(new_longitude_rad)

        return new_latitude, new_longitude
