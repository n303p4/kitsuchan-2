#!/usr/bin/env python3

"""This cog contains a Wikipedia query command."""

import urllib.parse

import discord
from discord.ext import commands

BASE_URL_WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php?{0}"


class Wikipedia:
    """Wikipedia command."""

    @commands.command(aliases=["wikipedia"])
    @commands.cooldown(6, 12, commands.BucketType.user)
    async def wiki(self, ctx, *, query: str):
        """Search Wikipedia.

        * query - A list of strings to be used in the search criteria.
        """
        params = urllib.parse.urlencode({"action": "opensearch", "search": query})
        url = BASE_URL_WIKIPEDIA_API.format(params)
        async with ctx.bot.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if not data[1]:
                    await ctx.send("No results found. :<")
                    return
                embed = discord.Embed()
                for index in range(0, min(3, len(data[1]))):
                    description = f"{data[3][index]}\n{data[2][index]}"
                    embed.add_field(name=data[1][index], value=description, inline=False)
                await ctx.send(embed=embed)
            else:
                message = "Couldn't reach Wikipedia. x.x"
                await ctx.send(message)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Wikipedia())
