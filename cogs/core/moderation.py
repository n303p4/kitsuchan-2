#!/usr/bin/env python3

"""Moderation extension."""

from discord.ext import commands

STATUS_INDICATORS = {"online": ":green_heart:",
                     "idle": ":yellow_heart:",
                     "dnd": ":heart:",
                     "offline": ":black_heart:"}
# This relies on Python 3.6's dictionary implementation to not break.
STATUS_SORTED = list(STATUS_INDICATORS.keys())


def _get_mods(ctx):
    the_mods = []
    for member in ctx.guild.members:
        if (ctx.channel.permissions_for(member).manage_messages and
                ctx.channel.permissions_for(member).kick_members and
                not member.bot):
            the_mods.append(member)
    return the_mods


class Moderation:
    """Moderation commands."""

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx):
        """Kick all users mentioned by this command.

        Requires both the user and bot to have `kick_members` to execute.
        """
        for member in ctx.message.mentions:
            await ctx.guild.kick(member)
        if ctx.message.mentions:
            await ctx.send("Kicked the requested members.")
        else:
            await ctx.send("No members mentioned.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx):
        """Ban all users mentioned by this command.

        Requires both the user and bot to have `ban_members` to execute.
        """
        for member in ctx.message.mentions:
            await ctx.guild.ban(member)
        if ctx.message.mentions:
            await ctx.send("Banned the requested members.")
        else:
            await ctx.send("No members mentioned.")

    @commands.command(aliases=["prune"])
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int):
        """Purge a certain number of messages from the channel.

        Requires both the user and bot to have `manage_messages` to execute.
        """
        limit += 1
        groups_100 = limit // 100
        groups_remainder = limit % 100
        for times in range(0, groups_100):
            await ctx.channel.purge(limit=100)
        await ctx.channel.purge(limit=groups_remainder)

    @commands.command(aliases=["moderators"])
    @commands.cooldown(1, 12, commands.BucketType.channel)
    async def mods(self, ctx):
        """Display moderators for the given channel.

        Assumes that members with `manage_messages`, `kick_members`, and `ban_members` are mods.
        """
        the_mods = _get_mods(ctx)
        message = ["**__Moderators__**"]
        for status in STATUS_INDICATORS:
            emote = STATUS_INDICATORS[status]
            mods_with_status = []
            for mod in the_mods:
                if mod.status.name == status:
                    mods_with_status.append(f"**{mod.name}**#{mod.discriminator}")
            if mods_with_status:
                message.append(f"{emote} " + ", ".join(mods_with_status))
        message = "\n".join(message)
        await ctx.send(message)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Moderation())
