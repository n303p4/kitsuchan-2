#!/usr/bin/env python3

from discord.ext import commands


class Ping:
    """Ping command."""

    @commands.command()
    @commands.cooldown(6, 12)
    async def ping(self, ctx):
        """Ping the bot."""
        current_shard_latency = ctx.bot.latencies[ctx.guild.shard_id]
        message = f"Current shard latency: {round(current_shard_latency[1]*1000, 2)} ms :fox:"
        await ctx.send(message)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Ping())
