#!/usr/bin/env python3

import datetime

from discord.ext import commands


class Ping:
    """Ping command."""

    @commands.command()
    @commands.cooldown(6, 12)
    async def ping(self, ctx):
        """Ping the bot."""
        pingtime = int(round((datetime.datetime.utcnow() -
                              ctx.message.created_at).total_seconds() * 1000, 0))
        message = f":ping_pong: {pingtime} ms!"
        await ctx.send(message)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Ping())
