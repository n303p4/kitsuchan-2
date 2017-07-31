#!/usr/bin/env python3

"""A command that ships two things together."""

from discord.ext import commands


class Ship:
    """A command that rates a ship."""

    @commands.command()
    @commands.cooldown(6, 12)
    async def ship(self, ctx, first_item, second_item):
        """Ship two things together."""
        rating = abs(hash(first_item) - hash(second_item)) % 101
        await ctx.send(f"I rate this ship a {rating}/100!")


def setup(bot):
    """Sets up the cog."""
    bot.add_cog(Ship())
