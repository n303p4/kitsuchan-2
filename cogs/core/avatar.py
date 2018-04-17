#!/usr/bin/env python3

"""Contains a cog that fetches user avatars."""

import discord
from discord.ext import commands

from k2 import helpers

VALID_SIZES = [16, 32, 64, 128, 256, 512, 1024]


class Avatar:
    """Avatar commands."""

    @commands.command()
    @commands.cooldown(6, 12)
    async def avatar(self, ctx, *, user: str = None):
        """Display a user's avatar.

        * user - A text string that the bot will attempt to use to look up a user."""
        if not user:
            user = ctx.author
        else:
            user = await helpers.member_by_substring(ctx, user)
        url = user.avatar_url
        if ".gif" in url:
            url = url + "&f=.gif"
        embed = discord.Embed(description=f"Avatar for {user.mention}")
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command(aliases=["gicon", "servericon", "sicon"])
    @commands.cooldown(6, 12)
    async def guildicon(self, ctx):
        """Display the icon of the current guild."""
        await ctx.send(ctx.guild.icon_url)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Avatar())
