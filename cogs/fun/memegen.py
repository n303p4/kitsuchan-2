#!/usr/bin/env python3

"""A cog containing a command that generates a meme out of someone."""

import discord
from discord.ext import commands

from k2 import helpers

BASE_URL_MEMEGEN = "https://memegen.link/custom/{0}/{1}.jpg?alt={2}"


class Memes:
    """A cog that contains a meme generator."""

    @commands.command(aliases=["usermeme", "um"])
    @commands.cooldown(6, 12)
    async def meme(self, ctx, thing: str, *, lines: str):
        """Generates a meme of a user or an image URL.
        Separate lines of text with a |.

        Example usage:

        kit meme @Kitsuchan#1024 I am | a meme
        """
        try:
            user = await helpers.member_by_substring(ctx, thing)
            image_url = user.avatar_url
        except commands.BadArgument:
            image_url = thing.strip("<>")
        lines = lines.split("|")
        if len(lines) < 2:
            await ctx.send("Please split the top and bottom lines with a |.")
            return
        for index, item in enumerate(lines):
            lines[index] = item.strip().replace(" ", "_")
        url = BASE_URL_MEMEGEN.format(lines[0], lines[1], image_url)
        print(url)
        embed = discord.Embed(title="Image link")
        embed.url = url
        embed.set_image(url=url)
        await ctx.send(embed=embed)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Memes())
