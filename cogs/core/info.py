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
            paginator = commands.Paginator(prefix="", suffix="")

            for permission, value in role.permissions:
                if value:
                    paginator.add_line(str(permission).capitalize().replace("_", " "))

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
