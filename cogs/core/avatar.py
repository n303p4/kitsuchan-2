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

        * user - A text string that the bot will attempt to use to look up a user.

        You may also specify a size for the. The size must be a power of 2 from 16 to 1024.

        User searches are done with substring matching, so if you're looking for a user called
        boingtheboingboing, you can simply run for example <prefix> avatar boing, where <prefix>
        is the bot's prefix. You may also mention the user or supply a user ID.

        Detailed behavior of this command is as follows (assuming you are the one issuing the
        command).

        * If no arguments are given, the avatar displayed is yours. E.g: kit avatar
        * If one argument is given and it's a valid size, the avatar displayed is yours, at that
        size. E.g: <prefix> avatar 512
        * If one argument is given and it's not a valid size, the bot will try to find a user
        whose ID or username matches it. E.g: <prefix> avatar b1nzy
        * If multiple arguments are given, and the final one is a valid size, the bot will try to
        find a user whose ID or username matches the rest of the arguments, and it will deliver
        it at the size specified. E.g: <prefix> avatar b1nzy the discord dev 512
        * If multiple arguments are given, and the final one is not a valid size, the bot will try
        to find a user whose ID or username matches all of the arguments. If it fails, it will
        omit the last argument and try searching with the rest of the arguments. If this too fails,
        the command will fail completely. E.g: <prefix> avatar b1nzy the discord dev
        * .gif avatars have fudged URLs so that they animate correctly in the client.
        """
        size = 1024  # Default size.
        if not user:
            user = ctx.author
        elif user.isdecimal() and int(user) in VALID_SIZES:
            size = int(user)
            user = ctx.author
        elif user.isdecimal():
            user = await helpers.member_by_substring(ctx, user)
        else:
            user_minus_last_word, sep, new_size = user.rpartition(" ")
            if new_size.isdecimal() and int(new_size) in VALID_SIZES:
                user = await helpers.member_by_substring(ctx, user_minus_last_word)
                size = int(new_size)
            else:
                try:
                    user = await helpers.member_by_substring(ctx, user)
                except commands.BadArgument:
                    user = await helpers.member_by_substring(ctx, user_minus_last_word)
        try:
            url = user.avatar_url_as(size=size)
            if ".gif" in url:
                url = url + "&f=.gif"
            embed = discord.Embed(description=f"Avatar for {user.mention}")
            embed.set_image(url=url)
            await ctx.send(embed=embed)
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
