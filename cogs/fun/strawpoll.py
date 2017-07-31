#!/usr/bin/env python3

"""A command that hooks strawpoll.me's API to create a poll."""

from discord.ext import commands

BASE_URL_STRAWPOLL = "https://strawpoll.me/{0}"
BASE_URL_STRAWPOLL_API = "https://strawpoll.me/api/v2/polls"


class Strawpoll:
    """Strawpoll command."""

    @commands.command(aliases=["strawpoll", "poll"])
    @commands.cooldown(6, 12)
    async def makepoll(self, ctx, *options):
        """Create a Straw Poll.

        Example usage:
        makepoll "Name of poll" "Option 1" "Option 2" Option3
        """
        options = " ".join(options).split(",")
        if len(options) < 3:
            return ("Please specify a title and at least two options. "
                    "Arguments must be separated with commas, e.g. "
                    "makepoll Test Poll, Option 1, Option 2")
        for index in range(0, len(options)):
            options[index] = options[index].strip()
        title = options.pop(0)
        data = {"title": title, "options": options}
        async with ctx.bot.session.request("POST", BASE_URL_STRAWPOLL_API, json=data) as response:
            if response.status <= 210:
                data = await response.json()
                url = BASE_URL_STRAWPOLL.format(data["id"])
                await ctx.send(f"Successfully created poll; you can find it at {url}")
            else:
                await ctx.send("Failed to create poll. x.x")


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Strawpoll())
