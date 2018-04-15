#!/usr/bin/env python3

"""Extension that handles kitsu.io queries.

Ported from Oxylibrium's Nestbot.
"""

import discord
from discord.ext import commands

from k2.helpers import query_web_api

BASE_URL_KITSUIO = "https://kitsu.io/api/edge/{0}"
FIELDS = {
    "Score": "averageRating",
    "Status": "status",
    "Started": "startDate"
}


def filter_request_type(request_type):
    if request_type not in ("anime", "manga"):
        request_type = "anime"
    return request_type


def generate_search_url(request_type):
    url = BASE_URL_KITSUIO.format(request_type)
    return url


class KitsuIO:
    """Cog that handles kitsu.io queries."""

    @commands.command(aliases=["manga", "anime"])
    async def kitsu(self, ctx, *, query: str):
        """Get manga or anime from kitsu.io"""
        request_type = filter_request_type(ctx.invoked_with)
        url = generate_search_url(request_type)

        params = {
            "filter[text]": query,
            "page[limit]": 1
        }

        response_content = await query_web_api(ctx.bot.session, url, service="kitsu.io",
                                               params=params)

        if response_content.get("meta", {}).get("count"):
            attributes = response_content["data"][0]["attributes"]
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
