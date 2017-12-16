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
    async def avatar(self, ctx, *, user: str=None):
        """Display a user's avatar.
        Defaults to displaying the avatar of the user who invoked the command.

        * user - A text string that the bot will attempt to use to look up a user.
        
        You may also specify a size for the avatar after the username, e.g. avatar kit 512
        """
        size = 1024
        if not user:
            user = ctx.author
        elif user.isdecimal():
            size = int(user)
            user = ctx.author
        else:
            user_minus_last_word, sep, new_size = user.rpartition(" ")
            if new_size.isdecimal():
                user = await helpers.member_by_substring(ctx, user_minus_last_word)
                size = int(new_size)
            else:
                user = await helpers.member_by_substring(ctx, user)
        try:
            await ctx.send(user.avatar_url_as(size=size))
        except discord.InvalidArgument:
            await ctx.send(f"Invalid size. Valid sizes: {VALID_SIZES}")

    @commands.command(aliases=["gicon", "servericon", "sicon"])
    @commands.cooldown(6, 12)
    async def guildicon(self, ctx):
        """Display the icon of the current guild."""
        await ctx.send(ctx.guild.icon_url)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Avatar())
