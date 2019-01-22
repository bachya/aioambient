"""Define fixtures for testing the REST API."""
import pytest


@pytest.fixture()
def device_details_json():
    """Define a response to /v1/devices/MAC_ADDRESS."""
    return [
        {
            "dateutc": 1547094300000,
            "winddir": 344,
            "windspeedmph": 1.6,
            "windgustmph": 2.2,
            "maxdailygust": 3.4,
            "tempf": 34,
            "hourlyrainin": 0,
            "eventrainin": 0,
            "dailyrainin": 0,
            "weeklyrainin": 0,
            "monthlyrainin": 0,
            "totalrainin": 0,
            "baromrelin": 30.38,
            "baromabsin": 24.89,
            "humidity": 49,
            "tempinf": 69.6,
            "humidityin": 30,
            "uv": 0,
            "solarradiation": 0,
            "feelsLike": 34,
            "dewPoint": 16.87,
            "date": "2019-01-10T04:25:00.000Z",
        },
        {
            "dateutc": 1547094000000,
            "winddir": 344,
            "windspeedmph": 0,
            "windgustmph": 0,
            "maxdailygust": 3.4,
            "tempf": 34,
            "hourlyrainin": 0,
            "eventrainin": 0,
            "dailyrainin": 0,
            "weeklyrainin": 0,
            "monthlyrainin": 0,
            "totalrainin": 0,
            "baromrelin": 30.38,
            "baromabsin": 24.89,
            "humidity": 50,
            "tempinf": 69.4,
            "humidityin": 29,
            "uv": 0,
            "solarradiation": 0,
            "feelsLike": 34,
            "dewPoint": 17.34,
            "date": "2019-01-10T04:20:00.000Z",
        },
    ]


@pytest.fixture()
def devices_json():
    """Define a response to /v1/devices."""
    return [
        {
            "macAddress": "84:F3:EB:21:90:C4",
            "lastData": {
                "dateutc": 1546889640000,
                "baromrelin": 30.09,
                "baromabsin": 24.61,
                "tempinf": 68.9,
                "humidityin": 30,
                "date": "2019-01-07T19:34:00.000Z",
            },
            "info": {
                "name": "Home",
                "location": "Home"
            },
        },
        {
            "macAddress": "84:F3:EB:21:90:C4",
            "lastData": {
                "dateutc": 1546889640000,
                "baromrelin": 30.09,
                "baromabsin": 24.61,
                "tempinf": 68.9,
                "humidityin": 30,
                "date": "2019-01-06T19:34:00.000Z",
            },
            "info": {
                "name": "Home",
                "location": "Home"
            },
        },
    ]
