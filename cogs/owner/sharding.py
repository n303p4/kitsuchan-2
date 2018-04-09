#!/usr/bin/env python3

"""Shard-related commands."""

import discord
from discord.ext import commands


class Sharding:
    """Shard information command. Bot owner only, used for diagnostics."""

    @commands.command()
    @commands.is_owner()
    async def shardinfo(self, ctx):
        embed = discord.Embed(title="Shard information")
        embed.add_field(name="Number of shards", value=ctx.bot.shard_count)
        embed.add_field(name="Shard serving this guild (first shard is 0)",
                        value=ctx.guild.shard_id)
        latency_string = "\n".join([f"Shard {t[0]}: {round(t[1]*1000, 2)}ms"
                                    for t in ctx.bot.latencies])
        embed.add_field(name="Latencies", value=latency_string)
        embed.add_field(name="Average latency", value=f"{round(ctx.bot.latency*1000, 2)}ms")
        await ctx.send(embed=embed)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Sharding())
