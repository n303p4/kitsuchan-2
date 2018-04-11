#!/usr/bin/env python3

"""A custom bot object."""

import json

import multio
from curious.core.client import Client

multio.init("curio")


class Bot(Client):
    """A custom bot object that provides a configuration handler and an aiohttp ClientSession.

    This is similar to k3.
    """

    def __init__(self, **kwargs):
        """In order for you to be able to initialize the token from config, this bot doesn't
        immediately initialize upon construction! You have to call `initialize_token` for that.

        In addition to everything supported by commands.Bot, this also supports:

        * `config_file` - An `str` representing the configuration file of the bot. Defaults to
                          `config.json`. This doesn't really have to be used, but it's there for
                          convenience reasons.

        Instance variables not in the constructor:

        * `config` - A `dict` containing key-value pairs meant for bot configuration. This doesn't
                     really have to be used, but it's there for convenience reasons.
        """
        self.config = {}
        self.config_file = kwargs.get("config_file", "config.json")

    def initialize_token(self, token):
        super().__init__(token)

    def load_config(self, filename: str = None):
        """Load config from a JSON file.

        * `filename` - The filename of the JSON file to be loaded. If not specified, the bot will
                       default to `Bot.config_file`.
        """
        if not filename:
            filename = self.config_file
        with open(filename) as file_object:
            config = json.load(file_object)
        if isinstance(config, dict):
            for key, value in config.items():
                self.config[key] = value

    def save_config(self, filename: str = None):
        """Save config to a JSON file.

        * `filename` - The filename of the JSON file to be saved to. If not specified, the bot will
                       default to `Bot.config_file`.
        """
        if not filename:
            filename = self.config_file
        with open(filename, "w") as file_object:
            json.dump(self.config, file_object, indent=4, sort_keys=True)
