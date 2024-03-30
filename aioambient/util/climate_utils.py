"""Climate utility functions."""

from __future__ import annotations

from math import log, sqrt
from typing import cast

MAGNUS_A = 17.27
MAGNUS_B = 237.7


class ClimateUtils:
    """Climate utility functions."""

    @staticmethod
    def convert_celsius_to_fahrenheit(celsius: float) -> float:
        """Convert celsius to fahrenheit.

        Args:
        ----
            celsius: Temperature measured in Celsius.

        Returns:
        -------
            Converted temperature measured in Fahrenheit.

        """
        return celsius * 9.0 / 5.0 + 32.0

    @staticmethod
    def convert_fahrenheit_to_celsius(fahrenheit: float) -> float:
        """Convert fahrenheit to celsius.

        Args:
        ----
            fahrenheit: Temperature measured in Fahrenheit.

        Returns:
        -------
            Converted temperature measured in Celsius.

        """
        return (fahrenheit - 32.0) * 5.0 / 9.0

    @staticmethod
    def convert_kph_to_mph(kph: float) -> float:
        """Convert kilometer per hour to miles per hour.

        Args:
        ----
            kph: Speed measured in kilometers per hour.

        Returns:
        -------
            Converted speed measured in miles per hour.

        """
        return kph * 0.621371192

    @staticmethod
    def dew_point_celsius(temp_celsius: float, humidity: float) -> float:
        """Calculate the dew point in Celsius.

        Args:
        ----
            temp_celsius: Temperature measured in Celsius.
            humidity: Relative humidity measured in percent.

        Returns:
        -------
            Calculated dew point measured in Celsius.

        """

        g = MAGNUS_A * temp_celsius / (MAGNUS_B + temp_celsius) + log(humidity / 100.0)
        return MAGNUS_B * g / (MAGNUS_A - g)

    @staticmethod
    def dew_point_fahrenheit(
        temp_fahrenheit: float | None, humidity: float | None
    ) -> float | None:
        """Calculate the dew point in Fahrenheit.

        Args:
        ----
            temp_fahrenheit: Temperature measured in Fahrenheit.
            humidity: Relative humidity measured in percent.

        Returns:
        -------
            Calculated dew point measured in Fahrenheit.

        """

        if temp_fahrenheit is None or humidity is None:
            return None

        humidity = min(humidity, 100)
        return ClimateUtils.convert_celsius_to_fahrenheit(
            ClimateUtils.dew_point_celsius(
                ClimateUtils.convert_fahrenheit_to_celsius(temp_fahrenheit),
                humidity,
            )
        )

    @staticmethod
    def _wind_chill_fahrenheit(temp_fahrenheit: float, wind_speed_mph: float) -> float:
        """Calculate the wind chill temperature in Fahrenheit.

        Args:
        ----
            temp_fahrenheit: Temperature measured in Fahrenheit.
            wind_speed_mph: Wind speed measured in miles per hour.

        Returns:
        -------
            Calculated wind chill measured in Fahrenheit.

        """

        return cast(
            float,
            35.74
            + 0.6215 * temp_fahrenheit
            - 35.75 * wind_speed_mph**0.16
            + 0.4275 * temp_fahrenheit * wind_speed_mph**0.16,
        )

    @staticmethod
    def _heat_index_fahrenheit(temp_fahrenheit: float, humidity: float) -> float:
        """Calculate the heat index temperature in Fahrenheit.

        Args:
        ----
            temp_fahrenheit: Temperature measured in Fahrenheit.
            humidity: Relative humidity measured in percent.

        Returns:
        -------
            Calculated heat index measured in Fahrenheit.

        """

        result = 0.5 * (
            temp_fahrenheit + 61 + (temp_fahrenheit - 68) * 1.2 + humidity * 0.094
        )

        if temp_fahrenheit < 80:
            return result

        heat_index_base = (
            -42.379
            + 2.04901523 * temp_fahrenheit
            + 10.14333127 * humidity
            + -0.22475541 * temp_fahrenheit * humidity
            + -0.00683783 * temp_fahrenheit * temp_fahrenheit
            + -0.05481717 * humidity * humidity
            + 0.00122874 * temp_fahrenheit * temp_fahrenheit * humidity
            + 0.00085282 * temp_fahrenheit * humidity * humidity
            + -0.00000199 * temp_fahrenheit * temp_fahrenheit * humidity * humidity
        )
        if humidity < 13 and temp_fahrenheit <= 112:
            return heat_index_base - (13 - humidity) / 4 * sqrt(
                (17 - (abs(temp_fahrenheit - 95))) / 17
            )

        if humidity > 85 and temp_fahrenheit <= 87:
            return heat_index_base + (humidity - 85) / 10 * ((87 - temp_fahrenheit) / 5)

        return heat_index_base

    @staticmethod
    def feels_like_fahrenheit(
        temp_fahrenheit: float | None,
        humidity: float | None,
        wind_speed_mph: float | None,
    ) -> float | None:
        """Calculate the feels like temperature in Fahrenheit.

        Args:
        ----
            temp_fahrenheit: Temperature measured in Fahrenheit.
            humidity: Relative humidity measured in percent.
            wind_speed_mph: Wind speed measured in miles per hour.

        Returns:
        -------
            Calculated feels like temperature measured in Fahrenheit.

        """

        if temp_fahrenheit is None or humidity is None or wind_speed_mph is None:
            return None

        if temp_fahrenheit < 50 and wind_speed_mph > 3:
            return ClimateUtils._wind_chill_fahrenheit(temp_fahrenheit, wind_speed_mph)

        if temp_fahrenheit > 68:
            return ClimateUtils._heat_index_fahrenheit(temp_fahrenheit, humidity)

        return temp_fahrenheit

    @staticmethod
    def feels_like_celsius(
        temp_celsius: float | None, humidity: float | None, wind_speed_kph: float | None
    ) -> float | None:
        """Calculate the feels like temperature in Celsius.

        Args:
        ----
            temp_celsius: Temperature measured in Celsius.
            humidity: Relative humidity measured in percent.
            wind_speed_kph: Wind speed measured in kilometers per hour.

        Returns:
        -------
            Calculated feels like temperature measured in Celsius.

        """

        if temp_celsius is None or humidity is None or wind_speed_kph is None:
            return None

        temp_fahrenheit = ClimateUtils.convert_celsius_to_fahrenheit(temp_celsius)
        wind_speed_mph = ClimateUtils.convert_kph_to_mph(wind_speed_kph)
        return ClimateUtils.convert_fahrenheit_to_celsius(
            # Result cannot be None, so cast it to float to avoid the mypy error:
            cast(
                float,
                ClimateUtils.feels_like_fahrenheit(
                    temp_fahrenheit, humidity, wind_speed_mph
                ),
            )
        )
