#!/usr/bin/env python3
# pylint: disable=C0103

"""Contains a cog for various weeb reaction commands."""
import random

import discord
from discord.ext import commands

from k2 import helpers
import owoe

systemrandom = random.SystemRandom()

BASE_URL_API_TYPES = "https://api.weeb.sh/images/types"
BASE_URL_API_TYPE = "https://api.weeb.sh/images/random?type={0}"
BASE_URL_API_TAG = "https://api.weeb.sh/images/random?tags={0}"


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
        """A weeb cog that builds reaction commands automatically."""
        self.bot = bot
        self.owoe = owoe.Owoe(token=self.bot.config["weebsh_token"], clientsession=self.bot.session)
        try:  # TODO this is hack
            self.bot.loop.run_until_complete(self.owoe.update_image_types())
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

            async def callback(self, ctx):
                url_image = await self.owoe.random_image(type_=ctx.command.name)
                embed = discord.Embed()
                embed.set_image(url=url_image)
                embed.set_footer(text="Powered by weeb.sh")
                await ctx.send(embed=embed)

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
    @commands.is_owner()
    async def weebupdate(self, ctx):
        """Update list of weeb.sh types. Bot owner only."""
        status = await self.owoe.update_image_types()
        if status:
            await ctx.send((f"Failed to update weeb.sh types with HTTP status code {status}. "
                            "It's possible that the endpoint is down."))
            return
        else:
            await ctx.send("Updated weeb.sh types successfully.")
        self._build_commands()
        for type_ in self.owoe.types:
            if type_ in self.bot.all_commands.keys():
                self.bot.remove_command(type_)
            self.bot.add_command(getattr(self, type_))


def setup(bot):
    """Setup function for reaction images."""
    bot.add_cog(Ram(bot))
