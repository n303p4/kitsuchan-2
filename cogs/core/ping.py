#!/usr/bin/env python3

from discord.ext import commands


class Ping:
    """Ping command."""

    @commands.command()
    @commands.cooldown(6, 12)
    async def ping(self, ctx):
        """Ping the bot."""
        msg = f"Current latency: {round(ctx.bot.latency*1000, 2)} ms :fox:"
        await ctx.send(msg)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Ping())
