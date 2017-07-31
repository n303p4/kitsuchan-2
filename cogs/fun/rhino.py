#!/usr/bin/env python3

"""An assorted collection of meme commands."""

import asyncio
import random

from discord.ext import commands

SUMMONABLES = {"Red-Eyes Black Dragon": "https://i.imgur.com/MiWwmqq.png",
               "Blue-Eyes White Dragon": "https://i.imgur.com/7LVixO3.png",
               "Exodia the Forbidden One": "https://i.imgur.com/wHWP34x.png",
               "Fox Fire": "https://i.imgur.com/xUIQmwa.png",
               "Bujingi Fox": "https://i.imgur.com/vFWak5N.png",
               "Lunalight Crimson Fox": "https://i.imgur.com/ReMqPsa.png",
               "Majespecter Fox - Kyubi": "https://i.imgur.com/5Yu8KJ7.png"}

systemrandom = random.SystemRandom()


class Rhino:
    """Various meme commands."""

    @commands.command()
    @commands.cooldown(6, 12)
    async def play(self, ctx):
        """Play?"""
        await ctx.send("Play with me? o.o")

    @commands.command(name="np", aliases=["noproblem"])
    @commands.cooldown(6, 12)
    async def np_(self, ctx):
        """No problem!"""
        await ctx.send("No problem! :3")

    @commands.command()
    @commands.cooldown(6, 12)
    async def pause(self, ctx):
        """Pause for a bit."""
        await ctx.send("...")
        await asyncio.sleep(5)
        await ctx.send("...? o.o")

    @commands.command()
    @commands.cooldown(6, 12)
    async def summon(self, ctx):
        """Summon a monster!"""
        name = systemrandom.choice(tuple(SUMMONABLES.keys()))
        image = SUMMONABLES[name]
        await ctx.send(f"I-I summon {name}! o.o\n{image}")


def setup(bot):
    """Sets up the cog."""
    bot.add_cog(Rhino())
