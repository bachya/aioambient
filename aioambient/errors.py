"""Define package errors."""


class AmbientError(Exception):
    """Define a base error."""


class RequestError(AmbientError):
    """Define an error related to invalid requests."""


class WebsocketError(AmbientError):
    """Define an error related to generic websocket errors."""
