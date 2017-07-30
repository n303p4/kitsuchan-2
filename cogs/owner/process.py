#!/usr/bin/env python3

"""Halt and restart commands."""

import sys
import os
import logging

from discord.ext import commands

logger = logging.getLogger(__name__)


class Process:
    """Commands that affect the bot's running process."""

    @commands.command(aliases=["shutdown", "kys"])
    @commands.is_owner()
    async def halt(self, ctx):
        """Halt the bot. Bot owner only."""
        if ctx.invoked_with == "kys":
            message = "Dead! x.x"
        else:
            message = "Bot is going for halt NOW!"
        logger.warning(message)
        await ctx.send(message)
        await ctx.bot.logout()

    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx):
        """Restart the bot. Bot owner only."""
        message = "Bot is going for restart NOW!"
        logger.warning(message)
        await ctx.send(message)
        await ctx.bot.logout()
        os.execl(sys.executable, sys.executable, *sys.argv)


def setup(bot):
    """Sets up the cog."""
    bot.add_cog(Process())