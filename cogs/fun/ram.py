#!/usr/bin/env python3
# pylint: disable=C0103

"""Contains a cog for various weeb reaction commands."""
import random

import discord
import requests
from discord.ext import commands

from k2 import helpers

systemrandom = random.SystemRandom()

BASE_URL_API_TYPES = "https://api.weeb.sh/images/types"
BASE_URL_API_TYPE = "https://api.weeb.sh/images/random?type={0}"
BASE_URL_API_TAG = "https://api.weeb.sh/images/random?tags={0}"
EMOJIS_KILL = (":gun:", ":knife:", ":eggplant:", ":bear:", ":fox:", ":wolf:", ":snake:",
               ":broken_heart:", ":crossed_swords:", ":fire:")


def _get_image_types(token: str=None):
    """Get image types."""
    headers = {"Authorization": f"Wolke {token}"}
    response = requests.get(BASE_URL_API_TYPES, headers=headers)  # TODO lmao requests
    if response.status_code == 200:
        return response.json()["types"]
    return []


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


async def _rra(ctx, kind: str, message: str="", usetag: bool=False):
    """A helper function that grabs an image and posts it in response to a user.

    * kind - The type of image to retrieve.
    * user - The member to mention in the command.
    """
    if usetag:
        url = BASE_URL_API_TAG.format(kind)
    else:
        url = BASE_URL_API_TYPE.format(kind)
    headers = {'Authorization': f"Wolke {ctx.bot.config.get('weebsh_token')}"}
    async with ctx.bot.session.get(url, headers=headers) as response:
        if response.status == 200:
            data = await response.json()
            url_image = data['url']
            embed = discord.Embed(title=message)
            embed.set_image(url=url_image)
            embed.set_footer(text="Powered by weeb.sh")
            await ctx.send(embed=embed)
        else:
            message = "Could not retrieve image. :("
            await ctx.send(message)


async def _send_image(ctx, url_image, message: str=""):
    """A helper function that creates an embed with an image and sends it off."""
    if isinstance(url_image, (tuple, list)):
        url_image = systemrandom.choice(url_image)
    embed = discord.Embed(title=message)
    embed.set_image(url=url_image)
    await ctx.send(embed=embed)


class Ram:
    """Weeb reaction commands."""

    def __init__(self, bot):
        """Procedurablly build reaction commands."""

        types = _get_image_types(bot.config["weebsh_token"])

        # TODO Add a help field to this mess.
        for key in types:

            # Avoid duplicate commands.
            if key in bot.all_commands.keys():
                continue

            helptext = f"{key.capitalize()}!"

            async def callback(self, ctx):
                await _rra(ctx, ctx.command.name)

            # Ew, gross.
            command = commands.command(name=key, help=helptext)(callback)
            command = commands.cooldown(6, 12, commands.BucketType.channel)(command)
            command.instance = self
            setattr(self, key, command)


def setup(bot):
    """Setup function for reaction images."""
    bot.add_cog(Ram(bot))
