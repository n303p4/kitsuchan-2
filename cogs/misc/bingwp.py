#!/usr/bin/env python3

import random

from discord.ext import commands

BASE_URL_BING_API = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n={0}&mkt=en-US"
BASE_URL_BING = "https://www.bing.com{0}"

systemrandom = random.SystemRandom()


class Wallpapers:
    """Bing wallpaper command."""

    @commands.command(aliases=["bwp"])
    @commands.cooldown(6, 12)
    async def bingwp(self, ctx):
        """Query Bing for a wallpaper."""

        url = BASE_URL_BING_API.format(8)

        async with ctx.bot.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                image = systemrandom.choice(data["images"])
                url = BASE_URL_BING.format(image["url"])
                await ctx.send(url)
            else:
                message = "Could not fetch wallpaper. :<"
                await ctx.send(message)


def setup(bot):
    """Sets up the cog."""
    bot.add_cog(Wallpapers())
