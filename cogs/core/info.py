#!/usr/bin/env python3

"""Informational commands."""

import resource
import sys

import discord
from discord.ext import commands

import k2
from k2 import helpers


class About:
    """Commands that display information about the bot, user, etc."""

    @commands.command(aliases=["botinfo", "binfo", "about", "stats"])
    @commands.cooldown(6, 12)
    async def info(self, ctx):
        """Display bot info, e.g. library versions."""

        embed = discord.Embed()
        embed.description = ctx.bot.description

        embed.set_thumbnail(url=ctx.bot.user.avatar_url_as(format="png", size=128))

        if k2:
            embed.add_field(name="Version", value=k2.version)

        ainfo = await ctx.bot.application_info()
        owner = str(ainfo.owner)
        embed.add_field(name="Owner", value=owner)

        embed.add_field(name="# of commands", value=len(ctx.bot.commands))

        if ctx.guild and ctx.bot.shard_count > 1:
            embed.add_field(name="Shard", value=f"{ctx.guild.shard_id+1} of {ctx.bot.shard_count}")

        num_guilds = len(ctx.bot.guilds)
        num_users = sum(not member.bot for member in ctx.bot.get_all_members())
        embed.add_field(name="Serving", value=f"{num_users} people in {num_guilds} guilds")

        embed.add_field(name="Python", value="{0}.{1}.{2}".format(*sys.version_info))
        embed.add_field(name="discord.py", value=discord.__version__)

        usage_memory = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000, 2)
        embed.add_field(name="Cookies eaten", value=f"{usage_memory} megabites")

        if k2:
            embed.add_field(name="Github", value=k2.url, inline=False)

        await ctx.send(embed=embed)

    @commands.command(brief="Display guild (server) info.",
                      aliases=["guild", "ginfo", "server", "serverinfo", "sinfo"])
    @commands.guild_only()
    @commands.cooldown(6, 12)
    async def guildinfo(self, ctx):
        """Display information about the current guild, such as owner, region, emojis, and roles."""

        guild = ctx.guild

        embed = discord.Embed(title=guild.name)
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

    @commands.command(brief="Display channel info.", aliases=["channel", "cinfo"])
    @commands.guild_only()
    @commands.cooldown(6, 12)
    async def channelinfo(self, ctx, *, channel: discord.TextChannel=None):
        """Display information about a text channel.
        Defaults to the current channel.

        * channel - Optional argument. A specific channel to get information about."""

        # If channel is None, then it is set to ctx.channel.
        channel = channel or ctx.channel

        embed = discord.Embed(title=f"{channel.name}")

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

    @commands.command(brief="Display voice channel info.",
                      aliases=["voicechannel", "vchannel", "vcinfo"])
    @commands.guild_only()
    @commands.cooldown(6, 12)
    async def vchannelinfo(self, ctx, *, channel: discord.VoiceChannel):
        """Display information about a voice channel.

        * channel - A specific voice channel to get information about."""

        embed = discord.Embed(title=f"{channel.name}")
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

    @commands.command(brief="Display user info.", aliases=["user", "uinfo"])
    @commands.guild_only()
    @commands.cooldown(6, 12)
    async def userinfo(self, ctx, *, user: str = None):
        """Display information about a user, such as status and roles.
        Defaults to the user who invoked the command.

        * user - Optional argument. A user in the current channel to get user information about."""
        if not user:
            user = ctx.author
        else:
            user = await helpers.member_by_substring(ctx, user)

        embed = discord.Embed(title=f"{str(user)}")
        embed.colour = user.color

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


def setup(bot):
    """Set up the extension."""
    bot.add_cog(About())
