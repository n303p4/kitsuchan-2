#!/usr/bin/env python3
# pylint: disable=C0103

"""Commands that invoke random things, part 2."""

import json
import random

from discord.ext import commands

URL_RANDOM_DOG_API = "https://random.dog/woof.json"
URL_RANDOM_CAT_API = "https://aws.random.cat/meow"
URL_RANDOM_BIRB = "https://random.birb.pw/img/{0}"
URL_RANDOM_BIRB_API = "https://random.birb.pw/tweet.json/"
URL_RANDOM_NEKO_API = "https://nekos.life/api/neko"

systemrandom = random.SystemRandom()


class RandomFun:
    """Commands that produce random outputs."""

    @commands.command(aliases=["doge"])
    @commands.cooldown(6, 12)
    async def dog(self, ctx):
        """Fetch a random dog."""
        async with ctx.bot.session.get(URL_RANDOM_DOG_API) as response:
            if response.status == 200:
                data = await response.text()
                doggo = json.loads(data)
                url = doggo["url"]
                await ctx.send(url)
            else:
                await ctx.send("Could not reach random.dog. :<")

    @commands.command(aliases=["feline"])
    @commands.cooldown(6, 12)
    async def cat(self, ctx):
        """Fetch a random cat."""
        message = "Command disabled. Please read this: http://random.cat/help.html"
        await ctx.send(message)

    @commands.command(aliases=["catgirl", "kneko", "nekomimi",
                               "foxgirl" "kitsune", "kitsunemimi"])
    @commands.cooldown(6, 12)
    async def kemono(self, ctx):
        """Fetch a random animal-eared person."""
        async with ctx.bot.session.get(URL_RANDOM_NEKO_API) as response:
            if response.status == 200:
                neko = await response.json()
                url = neko["neko"]
                await ctx.send(url)
            else:
                await ctx.send("Could not reach nekos.life. :<")

    @commands.command()
    @commands.cooldown(6, 12)
    async def birb(self, ctx):
        """Fetch a random birb."""
        async with ctx.bot.session.get(URL_RANDOM_BIRB_API) as response:
            if response.status == 200:
                data = await response.text()
                borb = json.loads(data)
                url = URL_RANDOM_BIRB.format(borb["file"])
                await ctx.send(url)
            else:
                await ctx.send("Could not reach random.birb.pw. :<")


def setup(bot):
    """Set up the extension."""
    bot.add_cog(RandomFun())
