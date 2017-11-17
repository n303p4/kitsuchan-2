#!/usr/bin/env python3

"""Contains a cog that fetches user avatars."""

import discord
from discord.ext import commands

from k2 import helpers


class Avatar:
    """Avatar commands."""

    @commands.command()
    @commands.cooldown(6, 12)
    async def avatar(self, ctx, *, user: str=None):
        """Display a user's avatar.
        Defaults to displaying the avatar of the user who invoked the command.

        * user - A member who you can mention for avatar."""
        if not user:
            user = ctx.author
        else:
            user = await helpers.member_by_substring(ctx, user)
        await ctx.send(user.avatar_url)

    @commands.command(aliases=["gicon", "servericon", "sicon"])
    @commands.cooldown(6, 12)
    async def guildicon(self, ctx):
        """Display the icon of the current guild."""
        await ctx.send(ctx.guild.icon_url)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Avatar())
