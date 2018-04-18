#!/usr/bin/env python3

"""Custom exceptions for Kitsuchan."""


class WebAPIException(Exception):
    """Base class for web API exceptions."""
    pass


class WebAPIUnreachable(WebAPIException):
    """This exception should be raised if a web API cannot be reached."""
    def __init__(self, *, service: str = None):
        super(WebAPIUnreachable, self).__init__()
        self.service = service
        self.default_message = f"Could not reach {self.service}."

    def __str__(self):
        return self.default_message


class WebAPIInvalidResponse(WebAPIException):
    """This exception should be raised if a web API cannot be reached."""
    def __init__(self, *, service: str = None):
        super(WebAPIInvalidResponse, self).__init__()
        self.service = service
        self.default_message = f"{self.service} returned an invalid response."

    def __str__(self):
        return self.default_message


class WebAPINoResultsFound(WebAPIException):
    """This exception should be raised if a web API cannot be reached."""
    def __init__(self, *, message: str = None):
        super(WebAPINoResultsFound, self).__init__()
        self._message = message if message else "No results found."

    def __str__(self):
        return self._message
