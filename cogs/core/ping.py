#!/usr/bin/env python3

"""Ping command for a discord.py rewrite bot."""

from discord.ext import commands


class Ping:
    """Ping command."""

    @commands.command()
    @commands.cooldown(6, 12)
    async def ping(self, ctx):
        """Ping the bot."""
        if ctx.guild and len(ctx.bot.latencies) > 1:
            current_shard_latency = ctx.bot.latencies[ctx.guild.shard_id]
            msg = (f"Average bot latency: {round(ctx.bot.latency*1000, 2)} ms :fox:\n"
                   f"Current shard latency: {round(current_shard_latency[1]*1000, 2)} ms :milk:")
        else:
            msg = f"Latency: {round(ctx.bot.latency*1000, 2)} ms :fox:"
        await ctx.send(msg)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Ping())
