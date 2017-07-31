#!/usr/bin/env python3

"""A minimal Discord bot made using discord.ext.commands.

Requires Python 3.6+ and discord.py rewrite (1.0).
"""

import os
import logging

from discord.ext import commands

from k2 import core

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

bot = core.Bot(command_prefix="", pm_help=True, config_file="config.json")


class IsNotHuman(commands.CommandError):
    """Raised if a bot attempts to invoke one of this bot's commands."""
    pass


@bot.check
def is_human(ctx):
    """Prevent the bot from responding to other bots."""
    if ctx.author.bot:
        raise IsNotHuman("User is not human")
    return True


@bot.listen("on_command_error")
async def handle_error(ctx, exc):
    """Simple error handler."""
    if not isinstance(exc, (commands.CommandNotFound, IsNotHuman)):
        await ctx.send(exc)

if __name__ == "__main__":
    bot.load_config()

    assert (isinstance(bot.config.get("discord_token"), str)), "Bot token not valid."
    assert (isinstance(bot.config.get("module_blacklist", []), list)), "Blacklist must be a list."

    prefix = bot.config.get("prefix", "k2")
    prefixes = [f"{prefix} ", prefix]
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
