#!/usr/bin/env python3
# pylint: disable=C0103

"""Contains a cog for various weeb reaction commands."""

import asyncio
import random

import discord
from discord.ext import commands
import owoe

from k2 import helpers

systemrandom = random.SystemRandom()


async def _generate_message(ctx, kind: str = None, user: str = None):
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
        """A weeb cog with reaction commands."""
        self.bot = bot
        self.owoe = owoe.Owoe(self.bot.config["weebsh_token"], self.bot.session)

        self.bot.loop.create_task(self._finish_init())

    async def _finish_init(self):
        """Notice that this does *not* properly handle HTTP status codes."""
        status_types = await self.owoe.update_image_types()
        status_tags = await self.owoe.update_image_tags()
        if status_types or status_tags:
            await asyncio.sleep(30)
            await self._finish_init()
        else:
            await self._build_commands()

    async def _build_commands(self):
        for key in self.owoe.types:

            # Avoid duplicate commands by removing them.
            if key in self.bot.all_commands.keys():
                self.bot.remove_command(key)

            helptext = f"Fetch random {key} image from weeb.sh."

            async def callback(self, ctx, *tags):
                tags = list(tags)
                for tag in tags:
                    if tag not in self.owoe.tags:
                        tags.remove(tag)
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
            self.bot.add_command(command)

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def weebtypes(self, ctx):
        """List all available weeb.sh types."""
        embed = discord.Embed(title="List of valid weeb.sh types")
        embed.description = ", ".join(self.owoe.types)[:2000]
        await ctx.send(embed=embed)

    @commands.command(aliases=["wt", "weebtag"])
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def weebtags(self, ctx, *set_of_tags):
        """List all available weeb.sh tags, or fetch an image by tag."""
        if not set_of_tags:
            embed = discord.Embed(title="List of valid weeb.sh tags")
            embed.description = ", ".join(self.owoe.tags)[:2000]
            embed.set_footer(text="You can use this command to fetch images by tags.")
            await ctx.send(embed=embed)
        else:
            url_image = await self.owoe.random_image(tags=set_of_tags)
            if isinstance(url_image, str):
                embed = discord.Embed()
                embed.set_image(url=url_image)
                embed.set_footer(text="Powered by weeb.sh")
                await ctx.send(embed=embed)
                return
            await ctx.send("No image matching your criteria was found.")


def setup(bot):
    """Setup function for reaction images."""
    bot.add_cog(Ram(bot))
