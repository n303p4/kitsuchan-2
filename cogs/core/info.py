#!/usr/bin/env python3

"""Additional informational commands for k2."""

import discord
from discord.ext import commands

from k2 import helpers


class Information:
    """Additional informational commands."""

    @commands.command(aliases=["rlist"])
    @commands.guild_only()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def roles(self, ctx):
        """Display a list of the guild's roles."""

        embed = discord.Embed(title=f"Roles: {len(ctx.guild.roles)}")
        embed.description = ", ".join([f"{r.name}" for r in ctx.guild.roles])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def whohas(self, ctx, *, role: str):
        """Display who has a given role.

        * role - The role to check for.
        """

        role = await helpers.role_by_substring(ctx, role)

        members_with_role = []
        for member in ctx.guild.members:
            if role in member.roles:
                members_with_role.append(member.mention)
        if members_with_role:
            await ctx.send("Nobody has that role. :<")
        else:
            embed = discord.Embed(title=f"Members with {role.name}: {len(members_with_role)}")
            embed.description = ", ".join(members_with_role)
            await ctx.send(embed=embed)

    @commands.command(brief="Display role info.", aliases=["rinfo"])
    @commands.guild_only()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def roleinfo(self, ctx, *, role: str):
        """Display information about a role.

        * role - The role to display information about."""

        role = await helpers.role_by_substring(ctx, role)

        embed = discord.Embed(title=role.name)
        embed.colour = role.color
        embed.description = f"{role.id} | Members: {len(role.members)}"
        embed.add_field(name="Color", value=f"{role.color}", inline=False)

        if role.permissions.administrator:
            embed.add_field(name="Administrator", value=True)

        else:
            # TODO THIS IS AWFUL
            permissions = {"Create instant invite": role.permissions.create_instant_invite,
                           "Kick members": role.permissions.kick_members,
                           "Ban members": role.permissions.ban_members,
                           "Administrator": role.permissions.administrator,
                           "Manage channels": role.permissions.manage_channels,
                           "Manage guild": role.permissions.manage_guild,
                           "Add reactions": role.permissions.add_reactions,
                           "View audit log": role.permissions.view_audit_log,
                           "Read messages": role.permissions.read_messages,
                           "Send messages": role.permissions.send_messages,
                           "Send TTS messages": role.permissions.send_tts_messages,
                           "Manage messages": role.permissions.manage_messages,
                           "Embed links": role.permissions.embed_links,
                           "Attach files": role.permissions.attach_files,
                           "Read message history": role.permissions.read_message_history,
                           "Mention everyone": role.permissions.mention_everyone,
                           "External emojis": role.permissions.external_emojis,
                           "Connect to voice channel": role.permissions.connect,
                           "Speak in voice channel": role.permissions.speak,
                           "Mute members": role.permissions.mute_members,
                           "Deafen members": role.permissions.deafen_members,
                           "Move members": role.permissions.move_members,
                           "Use voice activation": role.permissions.use_voice_activation,
                           "Change nickname": role.permissions.change_nickname,
                           "Manage nicknames": role.permissions.manage_nicknames,
                           "Manage roles": role.permissions.manage_roles,
                           "Manage webhooks": role.permissions.manage_webhooks,
                           "Manage emojis": role.permissions.manage_emojis}

            paginator = commands.Paginator(prefix="", suffix="")

            for key in permissions:
                if permissions[key]:
                    paginator.add_line(f"{key}")

            for page in paginator.pages:
                embed.add_field(name="Permissions", value=page)

        await ctx.send(embed=embed)

    @commands.command(aliases=["elist"])
    @commands.guild_only()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def emojis(self, ctx):
        """Display a list of the guild's custom emojis."""

        embed = discord.Embed(title=f"Custom emojis for {ctx.guild.name}")
        emoji_list = []
        for emoji in ctx.guild.emojis:
            emoji_list.append(str(emoji))
        embed.description = " ".join(emoji_list)
        await ctx.send(embed=embed)

    @commands.command(brief="Display custom emoji info.",
                      aliases=["emojiinfo", "einfo", "ceinfo"])
    @commands.guild_only()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def customemojiinfo(self, ctx, *, emoji: discord.Emoji):
        """Display information for a custom emoji.

        * emoji - The emoji to get information about."""

        embed = discord.Embed(title=emoji.name)
        embed.description = f"{emoji.id} | [Full image]({emoji.url})"

        embed.add_field(name="Guild", value=f"{emoji.guild.name} ({emoji.guild.id})")
        embed.add_field(name="Managed", value=emoji.managed)
        embed.add_field(name="Created at", value=emoji.created_at.ctime())

        embed.set_thumbnail(url=emoji.url)

        await ctx.send(embed=embed)


def setup(bot):
    """Setup function for Information."""
    bot.add_cog(Information())
