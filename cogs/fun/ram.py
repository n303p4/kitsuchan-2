#!/usr/bin/env python3
# pylint: disable=C0103

"""Contains a cog for various weeb reaction commands."""

import urllib.parse

import async_timeout
import requests
import discord
from discord.ext import commands

from k2.exceptions import WebAPIInvalidResponse, WebAPIUnreachable

BASE_URL_TYPES = "https://api.weeb.sh/images/types"
BASE_URL_RANDOM = "https://api.weeb.sh/images/random?{0}"


def get_types(headers):
    """Get image types from weeb.sh using requests."""
    response = requests.get(BASE_URL_TYPES, headers=headers)
    if response.status_code == 200:
        try:
            response_content = response.json()
            return response_content["types"]
        except Exception:
            raise WebAPIInvalidResponse(service="weeb.sh")
    raise WebAPIUnreachable(service="weeb.sh")


def generate_image_query_url(image_type):
    """Generate an image query URL for weeb.sh"""
    params = urllib.parse.urlencode({"type": image_type})
    url = BASE_URL_RANDOM.format(params)
    return url


async def random_image(session, url, headers):
    """Given a ClientSession and URL, query the URL and return its response content as a JSON."""
    async with async_timeout.timeout(10):
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                try:
                    response_content = await response.json()
                    return response_content
                except Exception:
                    raise WebAPIInvalidResponse(service="weeb.sh")
            raise WebAPIUnreachable(service="weeb.sh")


def setup(bot):
    """Set up the extension."""
    token = bot.config["weebsh_token"]
    headers = {"Authorization": f"Wolke {token}", **bot.headers}
    image_types = get_types(headers)

    class WeebSH:
        """Cog for interfacing weeb.sh"""

        @commands.command(aliases=image_types)
        async def weeb(self, ctx, image_type: str = None):
            """Fetch a random weeb.sh image. Can be used directly as an alias."""
            if ctx.invoked_with in image_types:
                image_type = ctx.invoked_with
            elif not image_type:
                image_type = ctx.invoked_with
            url = generate_image_query_url(image_type)
            try:
                response_content = await random_image(ctx.bot.session, url, headers)
            except WebAPIUnreachable:
                message = f"Invalid type supplied. Valid types are: ```{', '.join(image_types)}```"
                raise commands.UserInputError(message)
            else:
                embed = discord.Embed(title="Image link")
                embed.url = response_content["url"]
                embed.set_image(url=response_content["url"])
                embed.set_footer(text="Powered by weeb.sh")
                await ctx.send(embed=embed)

    bot.add_cog(WeebSH())
