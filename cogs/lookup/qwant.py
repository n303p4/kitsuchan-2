#!/usr/bin/env python3

"""This cog contains an image query command."""

import html
import random
import urllib.parse

import discord
from discord.ext import commands

BASE_URL_QWANT_API = "https://api.qwant.com/api/search/images?{0}"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0"
HEADERS = {"User-Agent": USER_AGENT}

systemrandom = random.SystemRandom()


class Qwant:
    """Qwant command."""

    def __init__(self, headers=None):
        self.headers = headers

    @commands.command(aliases=["qimage"])
    @commands.cooldown(6, 12)
    async def image(self, ctx, *, query: str):
        """Grab an image off the Internet using Qwant.

        * query - A string to be used in the search criteria.
        """
        params = urllib.parse.urlencode({"count": "100", "offset": "1", "q": query})
        url = BASE_URL_QWANT_API.format(params)
        async with ctx.bot.session.request("GET", url, headers=self.headers) as response:
            if response.status == 200:
                data = await response.json()
                if not data["data"]["result"]["items"]:
                    await ctx.send("No results found. :<")
                    return
                item = systemrandom.choice(data["data"]["result"]["items"])
                embed = discord.Embed(title=html.unescape(item["title"]))
                embed.description = item["url"]
                embed.set_image(url=item["media"])
                await ctx.send(embed=embed)
            else:
                message = "Couldn't reach Qwant. x.x"
                await ctx.send(message)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Qwant(headers=HEADERS))
