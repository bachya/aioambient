"""Define a client to interact with the Ambient Weather APIs."""
import logging
from typing import Optional

from aiohttp import ClientSession

from .api import API
from .websocket import Websocket

_LOGGER = logging.getLogger(__name__)

DEFAULT_API_VERSION = 1


class Client:  # pylint: disable=too-few-public-methods
    """Define the client."""

    def __init__(
        self,
        api_key: str,
        application_key: str,
        *,
        api_version: int = DEFAULT_API_VERSION,
        session: Optional[ClientSession] = None,
    ) -> None:
        """Initialize."""
        self.api: API = API(application_key, api_key, api_version, session)
        self.websocket: Websocket = Websocket(application_key, api_key, api_version)
