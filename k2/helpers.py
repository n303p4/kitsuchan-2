#!/usr/bin/env python3

"""Helper functions for Kitsuchan-NG and k2."""

import asyncio

import discord
from discord.ext import commands

MEMBERCONVERTER = commands.MemberConverter()
ROLECONVERTER = commands.RoleConverter()


async def yes_no(ctx: commands.Context,
                 message: str="Are you sure? Type **yes** within 10 seconds to confirm. o.o"):
    """Yes no helper. Ask a confirmation message with a timeout of 10 seconds.

    ctx - The context in which the question is being asked.
    message - Optional messsage that the question should ask.
    """
    await ctx.send(message)
    try:
        message = await ctx.bot.wait_for("message", timeout=10,
                                         check=lambda message: message.author == ctx.message.author)
    except asyncio.TimeoutError:
        await ctx.send("Timed out waiting. :<")
        return False
    if message.clean_content.lower() not in ["yes", "y"]:
        await ctx.send("Command cancelled. :<")
        return False
    return True


async def input_number(ctx: commands.Context,
                       message: str="Please enter a number within 10 seconds.",
                       *, timeout: int=10, min_value: int=None, max_value: int=None):
    """Input number helper. Ask a confirmation message with a timeout of 10 seconds.

    ctx - The context in which the question is being asked.
    message - Optional messsage that the question should ask.
    timeout - Timeout, in seconds, before automatically failing.
    min_value - Minimum accepted value for the input.
    max_value - Maximum accepted value for the input.
    """
    await ctx.send(message)

    def check(message):
        """A checking function dynamically to verify input."""
        if message.author != ctx.message.author or not message.clean_content.isdecimal():
            return False

        number = int(message.clean_content)

        if (min_value and number < min_value) or (max_value and number > max_value):
            return False

        return True

    try:
        message = await ctx.bot.wait_for("message", timeout=timeout, check=check)

    except asyncio.TimeoutError:
        raise commands.UserInputError("Timed out waiting.")

    return int(message.clean_content)


def is_moderator(ctx: commands.Context, member: discord.Member):
    """Check member permissions to decide if they're a moderator."""
    if (ctx.channel.permissions_for(member).manage_messages and
            ctx.channel.permissions_for(member).kick_members and not
            member.bot):
        return True
    return False


async def member_by_substring(ctx: commands.Context, substring: str):
    """This searches for a member by substrings."""
    try:
        return await MEMBERCONVERTER.convert(ctx, substring)
    except commands.CommandError:
        pass
    substring = substring.lower()
    for member in ctx.guild.members:
        if substring in member.name.lower() or substring in member.display_name.lower():
            return member
    raise commands.BadArgument(f"No user with substring `{substring}` was found.")


async def role_by_substring(ctx: commands.Context, substring: str):
    """This searches for a role by substrings."""
    try:
        return await ROLECONVERTER.convert(ctx, substring)
    except commands.CommandError:
        pass
    substring = substring.lower()
    for role in ctx.guild.roles:
        if substring in role.name.lower():
            return role
    raise commands.BadArgument(f"No role with substring `{substring}` was found.")
