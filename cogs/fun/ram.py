#!/usr/bin/env python3
# pylint: disable=C0103

"""Contains a cog for various weeb reaction commands."""
import random

import discord
import owoe
from discord.ext import commands

from k2 import helpers

systemrandom = random.SystemRandom()


async def _generate_message(ctx, kind: str=None, user: str=None):
    """Generate a message based on the user."""
    user = await helpers.member_by_substring(ctx, user)
    if not kind or not user:
        message = ""
    elif user.id == ctx.bot.user.id:
        message = f"Aw, thank you. Here, have one back. :3"
    elif user.id == ctx.author.id:
        message = systemrandom.choice(("Okay. :3",
                                       f"Sorry to see you're alone, have a {kind} anyway. :<",
                                       f"I'll {kind} your face alright. :3",
                                       ":<"))
    else:
        message = f"**{user.display_name}**, you got a {kind} from **{ctx.author.display_name}!**"
    return message


class Ram:
    """Weeb reaction commands."""

    def __init__(self, bot):
        """A weeb cog that builds reaction commands automatically.

        This is probably the hackiest cog in the bot. If it randomly breaks on reload, call
        the `weebupdate` command and it should fix things right up.
        """
        self.bot = bot
        self.owoe = owoe.Owoe(self.bot.config["weebsh_token"], self.bot.session)
        try:  # TODO this is hack
            self.bot.loop.run_until_complete(self.owoe.update_image_types())
            self.bot.loop.run_until_complete(self.owoe.update_image_tags())
            self._build_commands()
        except Exception:
            pass

    def _build_commands(self):
        """Internal use only. Procedurally builds all the commands."""
        for key in self.owoe.types:

            # Kill duplicate commands. `weebupdate` assumes that all the types are in this cog.
            if key in self.bot.all_commands.keys():
                self.bot.remove_command(key)

            helptext = f"Fetches a random image of category {key.capitalize().replace('_', ' ')}."

            async def callback(self, ctx, *tags):
                for tag in tags:
                    if tag not in self.owoe.tags:
                        await ctx.send("Invalid tag. Use the `weebtags` command for a list.")
                        return
                url_image = await self.owoe.random_image(type_=ctx.command.name, tags=tags)
                if isinstance(url_image, str):
                    embed = discord.Embed()
                    embed.set_image(url=url_image)
                    embed.set_footer(text="Powered by weeb.sh")
                    await ctx.send(embed=embed)
                    return
                await ctx.send("No image matching your criteria was found.")

            # Ew, gross.
            command = commands.command(name=key, help=helptext)(callback)
            command = commands.cooldown(6, 12, commands.BucketType.channel)(command)
            command.instance = self
            setattr(self, key, command)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def weebtypes(self, ctx):
        """List all available weeb.sh types."""
        embed = discord.Embed(title="List of valid weeb.sh types")
        embed.description = ", ".join(self.owoe.types)[:2000]
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def weebtags(self, ctx):
        """List all available weeb.sh tags."""
        embed = discord.Embed(title="List of valid weeb.sh tags")
        embed.description = ", ".join(self.owoe.tags)[:2000]
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def weebupdate(self, ctx):
        """Update list of weeb.sh types and tags. Bot owner only."""
        status = await self.owoe.update_image_types()
        await self.owoe.update_image_tags()
        if status:
            await ctx.send("Failed to reach the endpoint.")
            return
        else:
            await ctx.send("Updated from weeb.sh successfully.")
        self._build_commands()
        for type_ in self.owoe.types:
            if type_ in self.bot.all_commands.keys():
                self.bot.remove_command(type_)
            self.bot.add_command(getattr(self, type_))


def setup(bot):
    """Setup function for reaction images."""
    bot.add_cog(Ram(bot))
