#!/usr/bin/env python3

"""Contains a cog that spins a virtual fidget spinner."""

import asyncio
import random

import discord
from discord.ext import commands

systemrandom = random.SystemRandom()
spinners = []

FIDGET_SPINNERS = ("http://1.media.dorkly.cvcdn.com/98/93/8faa22b41bcbe455830907387af3a44b.gif",
                   "http://0.media.dorkly.cvcdn.com/20/80/4fcaa14e1215f43b4b791419dca027d9.gif",
                   ("https://vhs-talk.s3-us-west-2.amazonaws.com/original/2X/2/"
                    "2897b1847a18c33315d6d1f0066a6da590181988.gif"),
                   "http://fivedollarfidget.com/images/spinhandloop.gif",
                   "http://media.boingboing.net/wp-content/uploads/2017/02/good-spin.gif")


def is_not_spinning(ctx):
    if ctx.author.id in spinners:
        raise commands.UserInputError("You are already spinning!")
    return True


class Fidget:
    """Fidget spinner command."""

    @commands.command(aliases=["fidget", "spin"])
    @commands.cooldown(6, 12)
    @commands.check(is_not_spinning)
    async def spinner(self, ctx):
        """Spin a fidget spinner."""
        spinners.append(ctx.author.id)
        duration = systemrandom.randint(10, 200)
        message = f"{ctx.author.mention} spun a fidget spinner; let's see how long it lasts."
        spinner = systemrandom.choice(FIDGET_SPINNERS)
        embed = discord.Embed()
        embed.set_image(url=spinner)
        await ctx.send(message, embed=embed)
        await asyncio.sleep(duration)
        await ctx.send(f"{ctx.author.mention}, your spinner spun for {duration} seconds!")
        spinners.remove(ctx.author.id)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Fidget())
