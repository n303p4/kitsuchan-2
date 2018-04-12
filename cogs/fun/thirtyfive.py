#!/usr/bin/env python3
# pylint: disable=C0103

"""Commands inspired by Roadcrosser's bot 35."""

import random

from discord.ext import commands

systemrandom = random.SystemRandom()

AAA = ("a",
       "A",
       "\u3041",
       "\u3042",
       "\u30A1",
       "\u30A2")


class ThirtyFive:

    """This cog is a meme."""

    @commands.command(aliases=["aa", "aaa"])
    @commands.cooldown(10, 5, commands.BucketType.channel)
    async def a(self, ctx):
        """Aaaaaaa!"""
        message = systemrandom.choice(AAA) * systemrandom.randint(10, 200)
        await ctx.send(message)


def setup(bot):
    """Set up the 35 meme commands."""
    bot.add_cog(ThirtyFive())
