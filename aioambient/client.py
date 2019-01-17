"""Define a client to interact with the Ambient Weather APIs."""
# pylint: disable=unused-import
import logging
from typing import Dict, List, Union  # noqa

from aiohttp import ClientSession

from .api import API
from .const import API_VERSION

_LOGGER = logging.getLogger(__name__)

WEBSOCKET_ENDPOINT = '{0}/?api={1}&applicationKey={2}'


class Client:  # pylint: disable=too-few-public-methods
    """Define the client."""

    def __init__(
            self,
            api_key: str,
            application_key: str,
            websession: ClientSession,
            *,
            api_version: int = API_VERSION) -> None:
        """Initialize."""
        self.api = API(
            application_key, api_key, api_version, websession)
