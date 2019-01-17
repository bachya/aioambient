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

## REST API

The REST API of `aioambient` starts within an
[aiohttp](https://aiohttp.readthedocs.io/en/stable/) `ClientSession`:

```python
import asyncio

from aiohttp import ClientSession

from aioambient import Client


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
      # YOUR CODE HERE


asyncio.get_event_loop().run_until_complete(main())
```

Create a client, initialize it, then get to it:

```python
import asyncio

from aiohttp import ClientSession

from aioambient import Client


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
      client = Client(
        '<YOUR API KEY>',
        '<YOUR APPLICATION KEY>',
        websession)

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

Forthcoming!

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
