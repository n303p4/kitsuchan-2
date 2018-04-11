#!/usr/bin/env python3

"""Informational commands."""

import resource
import sys

import curious
from curious.commands.context import Context
from curious.commands.decorators import command
from curious.commands.plugin import Plugin
from curious.dataclasses.embed import Embed
from curious.dataclasses.member import Member

import k2


class About(Plugin):
    """Commands that display information about the bot, user, etc."""

    @command(aliases=["botinfo", "binfo", "about", "stats"])
    async def info(self, ctx: Context):
        """Display bot info, e.g. library versions."""

        embed = Embed()
        embed.description = ctx.bot.description

        embed.set_thumbnail(url=ctx.bot.user.avatar_url.as_format("png").with_size(128))

        embed.add_field(name="Version", value=k2.version)

        if ctx.guild and ctx.bot.get_shard_count() > 1:
            embed.add_field(name="Shard count", value=f"{ctx.bot.get_shard_count()}")

        num_guilds = len(ctx.bot.guilds)
        num_users = sum(not member.bot for member in ctx.bot.get_all_members())
        embed.add_field(name="Serving", value=f"{num_users} people in {num_guilds} guilds")

        embed.add_field(name="Python", value="{0}.{1}.{2}".format(*sys.version_info))
        embed.add_field(name="discord.py", value=curious.__version__)

        usage_memory = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000, 2)
        embed.add_field(name="Cookies eaten", value=f"{usage_memory} megabites")

        embed.add_field(name="Github", value=k2.url, inline=False)

        await ctx.send(embed=embed)

    @command(brief="Display guild (server) info.",
             aliases=["guild", "ginfo", "server", "serverinfo", "sinfo"])
    async def guildinfo(self, ctx: Context):
        """Display information about the current guild, such as owner, region, emojis, and roles."""

        guild = ctx.guild

        embed = Embed(title=guild.name)
        embed.description = guild.id

        embed.set_thumbnail(url=guild.icon_url)

        embed.add_field(name="Owner", value=str(guild.owner))

        embed.add_field(name="Members", value=len(ctx.guild.members))

        embed.add_field(name="Text channels", value=len(guild.text_channels))
        embed.add_field(name="Voice channels", value=len(guild.voice_channels))
        embed.add_field(name="Custom emojis", value=len(guild.emojis) or None)
        embed.add_field(name="Custom roles", value=len(guild.roles)-1 or None)
        embed.add_field(name="Region", value=str(guild.region))
        embed.add_field(name="Created at", value=guild.created_at.ctime())

        await ctx.send(embed=embed)

    @command(brief="Display channel info.", aliases=["channel", "cinfo"])
    async def channelinfo(self, ctx: Context):
        """Display information about a text channel.
        Defaults to the current channel.

        * channel - Optional argument. A specific channel to get information about."""

        # If channel is None, then it is set to ctx.channel.
        channel = channel or ctx.channel

        embed = Embed(title=f"{channel.name}")

        try:
            embed.description = channel.topic
        except AttributeError:
            pass

        embed.add_field(name="Channel ID", value=channel.id)

        try:
            embed.add_field(name="Guild", value=channel.guild.name)
        except AttributeError:
            pass

        embed.add_field(name="Members", value=len(channel.members))
        embed.add_field(name="Created at", value=channel.created_at.ctime())

        if channel.is_nsfw():
            embed.set_footer(text="NSFW content is allowed for this channel.")

        await ctx.send(embed=embed)

    @command(brief="Display voice channel info.",
             aliases=["voicechannel", "vchannel", "vcinfo"])
    async def vchannelinfo(self, ctx: Context):
        """Display information about a voice channel.

        * channel - A specific voice channel to get information about."""

        embed = Embed(title=f"{channel.name}")
        embed.add_field(name="Channel ID", value=channel.id)
        try:
            embed.add_field(name="Guild", value=channel.guild.name)
        except AttributeError:
            pass
        embed.add_field(name="Bitrate", value=f"{channel.bitrate}bps")
        if channel.user_limit > 0:
            user_limit = channel.user_limit
        else:
            user_limit = None
        embed.add_field(name="User limit", value=user_limit)
        embed.add_field(name="Created at", value=channel.created_at.ctime())
        await ctx.send(embed=embed)

    @command(brief="Display user info.", aliases=["user", "uinfo"])
    async def userinfo(self, ctx: Context, *, user: Member = None):
        """Display information about a user, such as status and roles.
        Defaults to the user who invoked the command.

        * user - Optional argument. A user in the current channel to get user information about."""
        if not user:
            user = ctx.author

        embed = Embed(title=f"{str(user)}")
        embed.colour = user.colour

        embed.description = str(user.id)
        if user.game:
            embed.description += f" | Playing **{user.game}**"

        embed.set_thumbnail(url=user.avatar_url_as(format="png", size=128))

        embed.add_field(name="Nickname", value=user.nick)
        embed.add_field(name="Bot user?", value="Yes" if user.bot else "No")

        # This is a bit awkward. Basically we don't want the bot to just say Dnd.
        if user.status.name == "dnd":
            status = "Do Not Disturb"
        else:
            status = user.status.name.capitalize()
        embed.add_field(name="Status", value=status)

        embed.add_field(name="Color", value=str(user.color))

        embed.add_field(name="Joined guild at", value=user.joined_at.ctime())
        embed.add_field(name="Joined Discord at", value=user.created_at.ctime())

        # This is crap.
        roles = ", ".join((role.name for role in user.roles if not role.is_default()))[:1024]
        if roles:
            embed.add_field(name="Roles", value=roles, inline=False)

        await ctx.send(embed=embed)
