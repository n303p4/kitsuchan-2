#!/usr/bin/env python3
# pylint: disable=C0103

"""A minimal Discord bot made using discord.ext.commands.

Requires Python 3.6+ and discord.py rewrite (1.0).
"""

import os
import json
import logging
import sys

import discord
from discord.ext import commands

import k2
from k2 import core

assert (os.geteuid() > 0), "Please don't run me as root. :<"
assert (sys.version_info >= (3, 6)), "I require Python 3.6 or higher. :3"
assert (discord.version_info >= (1, 0)), "I require discord.py 1.0 or higher. :3"

FORMAT = "%(asctime)-15s %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

DIRECTORY_PATH = os.path.dirname(os.path.realpath(__file__))

bot = core.Bot(command_prefix="", pm_help=False, config_file="config.json")


if __name__ == "__main__":

    if os.getcwd() != DIRECTORY_PATH and "-d" in sys.argv:
        os.chdir(DIRECTORY_PATH)

    try:
        bot.load_config()
    except json.decoder.JSONDecodeError:
        print("There seems to be an error in your config.json. Kitsuchan will now halt. :<")
        sys.exit()

    assert (isinstance(bot.config.get("discord_token"), str)), "Bot token not valid."
    assert (isinstance(bot.config.get("module_blacklist", []), list)), "Blacklist must be a list."

    bot.description = bot.config.get("description", k2.description)

    prefix = bot.config.get("prefix", "k2")
    prefixes = [
        f"{prefix} ",
        f"{prefix} ".capitalize(),
        prefix,
        prefix.capitalize()
    ]
    bot.command_prefix = commands.when_mentioned_or(*prefixes)

    blacklist = bot.config.get("module_blacklist", [])

    # Automatically load all modules.
    for dirpath, dirnames, filenames in os.walk("cogs"):
        for filename in filenames:
            if filename.endswith(".py"):
                fullpath = os.path.join(dirpath, filename).split(os.sep)
                module = ".".join(fullpath)[:-3]  # Eliminate the .py
                if module in blacklist:  # Skip blacklisted modules.
                    continue
                try:
                    bot.load_extension(module)
                except Exception as error:
                    print(f"Unable to load {module}: {error}")
    bot.run(bot.config["discord_token"])
