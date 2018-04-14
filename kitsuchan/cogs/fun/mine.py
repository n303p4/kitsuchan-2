#!/usr/bin/env python3
# pylint: disable=C0103

"""Contains a cog that handles tripmines."""

import asyncio
import random

import discord
from discord.ext import commands

systemrandom = random.SystemRandom()


class TripmineChannelArray:

    def __init__(self):
        self.array = []

    def has_member(self, user_id: int):
        """Checks is a member is in the array."""
        return user_id in self.array

    def add_member(self, user_id: int):
        """Adds a member to the array."""
        if user_id not in self.array:
            self.array.append(user_id)

    def remove_member(self, user_id: int):
        """Removes a member from the array."""
        if user_id in self.array:
            self.array.remove(user_id)

    @property
    def is_empty(self):
        """The length of the array is 0."""
        return not self.array


class Tripmine:
    """Set or remove a tripmine for someone."""

    def __init__(self, bot):

        self.tripmines = {}

        @bot.listen("on_message")
        async def tripmine(message):
            if message.author.id == bot.user.id:
                pass
            elif (message.channel.id in self.tripmines and
                  self.tripmines[message.channel.id].has_member(message.author.id)):
                explode = systemrandom.randint(1, 10)
                if explode == 1:
                    await message.channel.send((f":boom: {message.author.mention} **BOOM!** You "
                                                "got exploded by a tripmine! :boom:"))
                    self.tripmines[message.channel.id].remove_member(message.author.id)
                    if self.tripmines[message.channel.id].is_empty:
                        del self.tripmines[message.channel.id]

    @commands.command(aliases=["setmine", "tripmine"])
    @commands.cooldown(6, 12)
    async def mine(self, ctx, *, user: discord.Member):
        """Set a tripmine for someone. Tripmines go off at random.

        * user - The person for which the mine will go off.
        """
        if user.id == ctx.bot.user.id:
            await ctx.send("Nope. :3")
        elif (ctx.channel.id in self.tripmines.keys() and
              self.tripmines[ctx.channel.id].has_member(user.id)):
            raise commands.UserInputError(f"A tripmine is already set for {user.display_name}.")
        else:
            self.tripmines.setdefault(ctx.channel.id, TripmineChannelArray())
            self.tripmines[ctx.channel.id].add_member(user.id)
            message = await ctx.send(f"Tripmine set for {user.display_name}! :3")
            await asyncio.sleep(3)
            await message.delete()

    @commands.command(aliases=["unsetmine", "removemine"])
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def unmine(self, ctx, *, user: discord.Member):
        """Remove a tripmine from yourself, or from someone else.

        * user - The person for which the mine will go off.
        """
        if not user:
            user = ctx.author

        if user.id == ctx.bot.user.id:
            await ctx.send("Nope. :3")
        elif (ctx.channel.id in self.tripmines.keys() and
              self.tripmines[ctx.channel.id].has_member(user.id)):
            self.tripmines[ctx.channel.id].remove_member(user.id)
            await ctx.send(f"Removed tripmine for {user.display_name}! :3")
        else:
            raise commands.UserInputError(f"No tripmine is currently set for {user.display_name}.")


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Tripmine(bot))
