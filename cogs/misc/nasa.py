#!/usr/bin/env python3

from discord.ext import commands

BASE_URL_NASA_IOTD = "https://api.pandentia.cf/nasa/iotd"
BASE_URL_NASA_APOD = "https://api.pandentia.cf/nasa/apod"


class NASA:
    """NASA image commands."""

    @commands.command()
    @commands.cooldown(6, 12)
    async def iotd(self, ctx):
        """Fetch NASA's Image of the Day."""

        async with ctx.bot.session.get(BASE_URL_NASA_IOTD) as response:
            if response.status == 200:
                data = await response.json()
                response = data["response"]
                if response["image_url"]:
                    await ctx.send(response["image_url"])
                else:
                    await ctx.send(response["link"])
            else:
                message = "Could not fetch image. :<"
                await ctx.send(message)

    @commands.command()
    @commands.cooldown(6, 12)
    async def apod(self, ctx):
        """Fetch NASA's Astronomy Picture of the Day."""

        async with ctx.bot.session.get(BASE_URL_NASA_APOD) as response:
            if response.status == 200:
                data = await response.json()
                response = data["response"]
                if response["image_url"]:
                    await ctx.send(response["image_url"])
                else:
                    await ctx.send(response["link"])
            else:
                message = "Could not fetch image. :<"
                await ctx.send(message)


def setup(bot):
    """Sets up the cog."""
    bot.add_cog(NASA())
