# 🌤  aioambient: An async library for Ambient Weather Personal Weather Stations

[![Travis CI](https://travis-ci.org/bachya/aioambient.svg?branch=master)](https://travis-ci.org/bachya/aioambient)
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

* Python 3.5
* Python 3.6
* Python 3.7

However, running the test suite currently requires Python 3.6 or higher; tests
run on Python 3.5 will fail.

# API and Application Keys

Utilizing `aioambient` requires both an Application Key and an API Key from
Ambient Weather. You can generate both from the Profile page in your
[Ambient Weather Dashboard](https://dashboard.ambientweather.net).

# Usage

## Creating a Client

```python
import asyncio

from aioambient import Client


async def main() -> None:
  """Rock and roll."""
      client = Client('<YOUR API KEY>', '<YOUR APPLICATION KEY>')


asyncio.get_event_loop().run_until_complete(main())
```

If you have an existing `aiohttp.ClientSession`, you can use it:

```python
import asyncio

from aiohttp import ClientSession

from aioambient import Client


async def main() -> None:
  """Rock and roll."""
    async with ClientSession() as session:
      client = Client('<YOUR API KEY>', '<YOUR APPLICATION KEY>', session)


asyncio.get_event_loop().run_until_complete(main())
```

## REST API

```python
import asyncio

from aioambient import Client


async def main() -> None:
  """Rock and roll."""
    client = Client('<YOUR API KEY>', '<YOUR APPLICATION KEY>')

    # Get all devices in an account:
    await client.api.get_devices()

    # Get all stored readings from a device:
    await client.api.get_device_details('<DEVICE MAC ADDRESS>')

    # Get all stored readings from a device (starting at a datetime):
    await client.api.get_device_details(
      '<DEVICE MAC ADDRESS>', end_date="2019-01-16")


asyncio.get_event_loop().run_until_complete(main())
```

Please be aware of Ambient Weather's
[rate limiting policies](https://ambientweather.docs.apiary.io/#introduction/rate-limiting).

## Websocket API

```python
import asyncio

from aioambient import Client


async def main() -> None:
    """Rock and roll."""
    client = Client( '<YOUR API KEY>', '<YOUR APPLICATION KEY>')

    # Define a method (sync or async) that should be run when the websocket
    # client connects:
    def connect_method():
        """Print a simple "hello" message."""
        print('Client has connected to the websocket')
    client.websocket.on_connect(connect_method)

    # Define a method (sync or async) that should be run upon subscribing to
    # the Ambient Weather cloud:
    def subscribed_method(data):
        """Print the data received upon subscribing."""
        print('Subscription data received: {0}'.format(data))
    client.websocket.on_subscribed(subscribed_method)

    # Define a method (sync or async) that should be run upon receiving data:
    def data_method(data):
        """Print the data received."""
        print('Data received: {0}'.format(data))
    client.websocket.on_data(data_method)

    # Define a method (sync or async) that should be run when the websocket
    # client disconnects:
    def disconnect_method(data):
        """Print a simple "goodbye" message."""
        print('Client has disconnected from the websocket')
    client.websocket.on_disconnect(disconnect_method)

    # Connect to the websocket:
    await client.websocket.connect()

    # At any point, disconnect from the websocket:
    await client.websocket.disconnect()


loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()
```

# Contributing

1. [Check for open features/bugs](https://github.com/bachya/aioambient/issues)
  or [initiate a discussion on one](https://github.com/bachya/aioambient/issues/new).
2. [Fork the repository](https://github.com/bachya/aioambient/fork).
3. Install the dev environment: `make init`.
4. Enter the virtual environment: `pipenv shell`
5. Code your new feature or bug fix.
6. Write a test that covers your new functionality.
7. Run tests and ensure 100% code coverage: `make coverage`
8. Add yourself to `AUTHORS.md`.
9. Submit a pull request!
