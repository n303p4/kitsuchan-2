#!/usr/bin/env python3

"""A dead simple aiohttp-based library for weeb.sh. Nothing more. Honest."""

import urllib
import asyncio

import aiohttp

BASE_URL_TYPES = "https://api.weeb.sh/images/types"
BASE_URL_RANDOM = "https://api.weeb.sh/images/random?{0}"


class InvalidImageType(Exception):
    """Raised if the image type is not valid."""
    pass


class Owoe:
    """A class that contains a simple interface for weeb.sh.

    This will typically be used compositionally, as a component of a larger class.
    """

    def __init__(self, token: str=None, clientsession: aiohttp.ClientSession=None):
        """Constructor method for `Owoe`.

        * `token` - An `str` containing your token from Wolke.
        * `clientsession` - An optional `aiohttp.ClientSession` to use Owoe with another program. If
                            not supplied, Owoe will create one for itself to be used standalone.

        **Fields not in the constructor**

        * `types` - A `list` of `str` containing all valid image types. It's recommended not to
                    update this yourself; instead, call `update_image_types()`. Owoe will not work
                    if you do not have this `list` populated.
        * `headers` - A `dict` for simple HTTP authorization.
        """
        self.token = token
        self.headers = {"Authorization": f"Wolke {token}"}
        self.types = []
        if not clientsession:
            loop = asyncio.get_event_loop()
            self.clientsession = aiohttp.ClientSession(loop=loop)
        else:
            self.clientsession = clientsession

    async def update_image_types(self):
        """Update the image types `list` by calling the `/types` endpoint. This is a coroutine.

        You must call this to populate the types `list`, otherwise Owoe will not work.

        If successful, returns a `None`, otherwise returns an `int` with an HTTP status code.
        """
        async with self.clientsession.get(BASE_URL_TYPES, headers=self.headers) as response:
            if response.status == 200:
                data = await response.json()
                types = data["types"]
                self.types = []
                for type_ in types:
                    self.types.append(type_)
                return
            return response.status

    async def random_image(self, type_: str, tags: str):
        """Get a random image from weeb.sh by calling the `/random` endpoint. This is a coroutine.

        Possible return values are as follows:

        * If `type_` is not valid, raises an `Owoe.InvalidImageType` error.
        * If successful, returns an `str` with the URL of the image.
        * If an HTTP status error occurs, returns an `int` with the status code.

        * `type_` - An `str` representing the type of the image to be obtained.
                    Must be in `self.types`. Has an underscore to avoid colliding with
                    built-in Python `type`.
        * `tags` - An `str` representing a list of tags to use in the image search.
        """
        if type_ not in self.types:
            raise InvalidImageType()

        parameters_url = {}
        if type_:
            parameters_url["type"] = type_
        if tags:
            parameters_url["tags"] = tags

        parameters_url = urllib.parse.urlencode(parameters_url)

        url_random = BASE_URL_RANDOM.format(parameters_url)

        async with self.clientsession.get(url_random, headers=self.headers) as response:
            if response.status == 200:
                data = await response.json()
                url_image = data["url"]
                return url_image
            return response.status
