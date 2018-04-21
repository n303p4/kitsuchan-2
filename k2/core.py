#!/usr/bin/env python3

"""A custom bot object."""

import json

import aiohttp
from discord.ext import commands

import k2


class Bot(commands.AutoShardedBot):
    """A custom bot object that provides a configuration handler and an aiohttp ClientSession.

    This is similar to k3.
    """

    def __init__(self, *args, **kwargs):
        """In addition to everything supported by commands.Bot, this also supports:

        * `config_file` - An `str` representing the configuration file of the bot. Defaults to
                          `config.json`. This doesn't really have to be used, but it's there for
                          convenience reasons.

        Instance variables not in the constructor:

        * `session` - An `aiohttp.ClientSession` that the bot can use to make HTTP requests.
                      This is useful for commands that perform API hooks.
        * `config` - A `dict` containing key-value pairs meant for bot configuration. This doesn't
                     really have to be used, but it's there for convenience reasons.
        """
        super().__init__(*args, **kwargs)
        self.config = {}
        self.config_file = kwargs.get("config_file", "config.json")
        self.headers = {"User-Agent": f"Kitsuchan/{k2.version_number}"}
        self.session = aiohttp.ClientSession(loop=self.loop, headers=self.headers)

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
