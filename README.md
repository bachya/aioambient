# 🌤  aioambient: An async library for Ambient Weather Personal Weather Stations

[![CI](https://github.com/bachya/aioambient/workflows/CI/badge.svg)](https://github.com/bachya/aioambient/actions)
[![PyPi](https://img.shields.io/pypi/v/aioambient.svg)](https://pypi.python.org/pypi/aioambient)
[![Version](https://img.shields.io/pypi/pyversions/aioambient.svg)](https://pypi.python.org/pypi/aioambient)
[![License](https://img.shields.io/pypi/l/aioambient.svg)](https://github.com/bachya/aioambient/blob/master/LICENSE)
[![Code Coverage](https://codecov.io/gh/bachya/aioambient/branch/dev/graph/badge.svg)](https://codecov.io/gh/bachya/aioambient)
[![Maintainability](https://api.codeclimate.com/v1/badges/81a9f8274abf325b2fa4/maintainability)](https://codeclimate.com/github/bachya/aioambient/maintainability)
[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)

`aioambient` is a Python3, asyncio-driven library that interfaces with both the
REST and Websocket APIs provided by
[Ambient Weather](https://ambientweather.net).

# Installation

```python
pip install aioambient
```

# Python Versions

`aioambient` is currently supported on:

* Python 3.7
* Python 3.8
* Python 3.9
* Python 3.10

# API and Application Keys

Utilizing `aioambient` requires both an Application Key and an API Key from
Ambient Weather. You can generate both from the Profile page in your
[Ambient Weather Dashboard](https://dashboard.ambientweather.net).

# Usage

## REST API

```python
import asyncio
from datetime import date

from aiohttp import ClientSession

from aioambient import API


async def main() -> None:
    """Create the aiohttp session and run the example."""
    api = API("<YOUR APPLICATION KEY>", "<YOUR API KEY>")

    # Get all devices in an account:
    await api.get_devices()

    # Get all stored readings from a device:
    await api.get_device_details("<DEVICE MAC ADDRESS>")

    # Get all stored readings from a device (starting at a datetime):
    await api.get_device_details(
        "<DEVICE MAC ADDRESS>", end_date=date(2019, 1, 16)
    )


asyncio.run(main())
```

By default, the library creates a new connection to Ambient Weather with each coroutine.
If you are calling a large number of coroutines (or merely want to squeeze out every
second of runtime savings possible), an
[`aiohttp`](https://github.com/aio-libs/aiohttp) `ClientSession` can be used for connection
pooling:

```python
import asyncio
from datetime import date

from aiohttp import ClientSession

from aioambient import API


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as session:
        api = API("<YOUR APPLICATION KEY>", "<YOUR API KEY>")

        # Get all devices in an account:
        await api.get_devices()

        # Get all stored readings from a device:
        await api.get_device_details("<DEVICE MAC ADDRESS>")

        # Get all stored readings from a device (starting at a datetime):
        await api.get_device_details(
            "<DEVICE MAC ADDRESS>", end_date=date(2019, 1, 16)
        )


asyncio.run(main())
```

Please be aware of Ambient Weather's
[rate limiting policies](https://ambientweather.docs.apiary.io/#introduction/rate-limiting).

## Websocket API

```python
import asyncio

from aiohttp import ClientSession

from aioambient import Websocket


async def main() -> None:
    """Create the aiohttp session and run the example."""
    websocket = Websocket("<YOUR APPLICATION KEY>", "<YOUR API KEY>")

    # Note that you can watch multiple API keys at once:
    websocket = Websocket("YOUR APPLICATION KEY", ["<API KEY 1>", "<API KEY 2>"])

    # Define a method that should be fired when the websocket client
    # connects:
    def connect_method():
        """Print a simple "hello" message."""
        print("Client has connected to the websocket")

    websocket.on_connect(connect_method)

    # Alternatively, define a coroutine handler:
    async def connect_coroutine():
        """Waits for 3 seconds, then print a simple "hello" message."""
        await asyncio.sleep(3)
        print("Client has connected to the websocket")

    websocket.async_on_connect(connect_coroutine)

    # Define a method that should be run upon subscribing to the Ambient
    # Weather cloud:
    def subscribed_method(data):
        """Print the data received upon subscribing."""
        print(f"Subscription data received: {data}")

    websocket.on_subscribed(subscribed_method)

    # Alternatively, define a coroutine handler:
    async def subscribed_coroutine(data):
        """Waits for 3 seconds, then print the incoming data."""
        await asyncio.sleep(3)
        print(f"Subscription data received: {data}")

    websocket.async_on_subscribed(subscribed_coroutine)

    # Define a method that should be run upon receiving data:
    def data_method(data):
        """Print the data received."""
        print(f"Data received: {data}")

    websocket.on_data(data_method)

    # Alternatively, define a coroutine handler:
    async def data_coroutine(data):
        """Wait for 3 seconds, then print the data received."""
        await asyncio.sleep(3)
        print(f"Data received: {data}")

    websocket.async_on_data(data_coroutine)

    # Define a method that should be run when the websocket client
    # disconnects:
    def disconnect_method(data):
        """Print a simple "goodbye" message."""
        print("Client has disconnected from the websocket")

    websocket.on_disconnect(disconnect_method)

    # Alternatively, define a coroutine handler:
    async def disconnect_coroutine(data):
        """Wait for 3 seconds, then print a simple "goodbye" message."""
        await asyncio.sleep(3)
        print("Client has disconnected from the websocket")

    websocket.async_on_disconnect(disconnect_coroutine)

    # Connect to the websocket:
    await websocket.connect()

    # At any point, disconnect from the websocket:
    await websocket.disconnect()


asyncio.run(main())
```

# Contributing

1. [Check for open features/bugs](https://github.com/bachya/aioambient/issues)
  or [initiate a discussion on one](https://github.com/bachya/aioambient/issues/new).
2. [Fork the repository](https://github.com/bachya/aioambient/fork).
3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`
4. (_optional, but highly recommended_) Enter the virtual environment: `source ./venv/bin/activate`
5. Install the dev environment: `script/setup`
6. Code your new feature or bug fix.
7. Write tests that cover your new functionality.
8. Run tests and ensure 100% code coverage: `nox -rs coverage`
9. Update `README.md` with any new documentation.
10. Add yourself to `AUTHORS.md`.
11. Submit a pull request!
