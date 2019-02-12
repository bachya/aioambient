"""Define package errors."""


class AmbientError(Exception):
    """Define a base error."""

    pass


class RequestError(AmbientError):
    """Define an error related to invalid requests."""

    pass


class WebsocketError(AmbientError):
    """Define an error related to generic websocket errors."""

    pass
