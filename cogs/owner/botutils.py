#!/usr/bin/env python3

"""Bot utility commands."""

import os

import discord
from discord.ext import commands


class Utilities:
    """Utility commands for the bot owner.

    These commands will not show up in the help unless you're the owner.
    """

    @commands.command()
    @commands.is_owner()
    async def rename(self, ctx, *, username):
        """Change the bot's username. Bot owner only.

        * username - The new username to assign the bot.
        """
        await ctx.bot.user.edit(username=username)
        await ctx.send(f"Username changed. :3")

    @commands.command()
    @commands.is_owner()
    async def setavatar(self, ctx, *, filename):
        """Change the bot's avatar. Bot owner only.

        * filename - The filename of the avatar to assign the bot.
        """
        if os.path.isfile(filename):
            with open(filename, "rb") as fileobject:
                avatar = fileobject.read()
            await ctx.bot.user.edit(avatar=avatar)
            await ctx.send("Avatar changed, hopefully. :<")
        else:
            raise commands.UserInputError("Not a valid filename.")

    @commands.command()
    @commands.is_owner()
    async def setgame(self, ctx, *, game_name=None):
        """Change the bot's playing status. Bot owner only.

        * game_name - The text to display in the playing status.
        """
        if game_name:
            game = discord.Game(name=game_name)
            await ctx.bot.change_presence(activity=game)
        else:
            await ctx.bot.change_presence(game=None)
        await ctx.send("Game set. :3")

    @commands.command(aliases=["clean"])
    @commands.is_owner()
    async def censor(self, ctx, times: int = 1):
        """Delete the bot's previous message(s). Bot owner only.

        * times - Number of message to delete. Defaults to 1.
        """
        if times < 1:
            return commands.UserInputError("Can't delete less than 1 message.")
        times_executed = 0
        async for message in ctx.channel.history():
            if times_executed == times:
                break
            if message.author.id == ctx.bot.user.id:
                await message.delete()
                times_executed += 1

    @commands.command(aliases=["say"])
    @commands.is_owner()
    async def echo(self, ctx, *, text=""):
        """Repeat the user's text back at them. Bot owner only.

        * text - A string to be echoed back.
        """
        if not text:
            text = "Echo?"
        # This mostly prevents the bot from triggering other bots.
        text = "\u200B" + text
        await ctx.send(text)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Utilities())
