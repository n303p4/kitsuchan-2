#!/usr/bin/env python3

"""Extension that handles kitsu.io queries.

Ported from Oxylibrium's Nestbot.
"""

import discord
from discord.ext import commands

BASE_URL_KITSUIO = "https://kitsu.io/api/edge/{0}"
FIELDS = {
    "Score": "averageRating",
    "Status": "status",
    "Started": "startDate"
}


class KitsuIO:
    """Cog that handles kitsu.io queries."""

    @commands.command(aliases=["manga", "anime"])
    async def kitsu(self, ctx, *, query: str):
        """Get manga or anime from kitsu.io"""
        request_type = "anime" if ctx.invoked_with == "kitsu" else ctx.invoked_with
        url = BASE_URL_KITSUIO.format(request_type)

        params = {
            "filter[text]": query,
            "page[limit]": 1
        }

        async with ctx.bot.session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json(content_type="application/vnd.api+json")
            else:
                await ctx.send("Could not reach kitsu.io x.x")
                return

        if data.get("meta", {}).get("count"):
            attributes = data["data"][0]["attributes"]
            link = f"https://kitsu.io/{request_type}/{attributes['slug']}"
            titles = (f"{attributes['titles'].get('en', '???')} - "
                      f"{attributes['titles'].get('en_jp', '???')}")

            embed = discord.Embed(title=titles,
                                  url=link,
                                  description=attributes.get("synopsis", "None"))

            for name, item in FIELDS.items():
                embed.add_field(name=name, value=attributes.get(item, "N/A"))

            if attributes.get("endDate"):
                embed.add_field(name="Finished", value=attributes["endDate"])
            try:
                embed.set_thumbnail(url=attributes["posterImage"]["original"])
            except KeyError:
                pass

            await ctx.send(embed=embed)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(KitsuIO())
