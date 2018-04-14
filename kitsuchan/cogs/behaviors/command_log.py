#!/usr/bin/env python3
# pylint: disable=C0103

"""Command logging functionality."""

import logging

FORMAT = "%(asctime)-15s: %(message)s"
formatter = logging.Formatter(FORMAT)

logger = logging.getLogger('commands.log')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("commands.log")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)


def setup(bot):
    """Sets up the extension."""

    @bot.listen("on_command")
    async def log_command(ctx):
        message = (f"{ctx.message.content} | "
                   f"{ctx.author.id} in {ctx.guild.name}:{ctx.guild.id}")
        logger.info(message)
        message = f"{ctx.message.created_at.ctime()}: {message}"
