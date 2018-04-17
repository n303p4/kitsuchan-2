#!/usr/bin/env python3

"""Extension that handles kitsu.io queries.

Ported from Oxylibrium's Nestbot.
"""

import async_timeout
import discord
from discord.ext import commands

from k2.exceptions import WebAPIInvalidResponse, WebAPIUnreachable

BASE_URL_KITSUIO = "https://kitsu.io/api/edge/{0}"
FIELDS = {
    "Score": "averageRating",
    "Status": "status",
    "Started": "startDate"
}


def filter_request_type(request_type):
    """Given an arbitrary string, generate a valid request type for kitsu.io."""
    return request_type


def generate_search_url(request_type):
    """Given a request type, generate a query URL for kitsu.io."""
    if request_type not in ("anime", "manga"):
        request_type = "anime"
    url = BASE_URL_KITSUIO.format(request_type)
    return url


async def search(session, url, params):
    """Given a ClientSession and URL, query the URL and return its response content as a JSON."""
    async with async_timeout.timeout(10):
        async with session.get(url, params=params) as response:
            if response.status == 200:
                try:
                    resp_content = await response.json(content_type="application/vnd.api+json")
                except Exception:
                    raise WebAPIInvalidResponse(service="kitsu.io")
            else:
                raise WebAPIUnreachable(service="kitsu.io")

    return resp_content


def generate_parsed_result(response_content, request_type):
    """Parse response content from kitsu.io and return a dict."""
    try:
        attributes = response_content["data"][0]["attributes"]

        result = {
            "title_english": f"{attributes['titles'].get('en', '???')}",
            "title_romaji": f"{attributes['titles'].get('en_jp', '???')}",
            "url": f"https://kitsu.io/{request_type}/{attributes['slug']}",
            "description": attributes.get("synopsis", "None"),
            "fields": {}
        }

        for name, item in FIELDS.items():
            result["fields"][name] = attributes.get(item, "N/A")

        if attributes.get("endDate"):
            result["fields"]["Finished"] = attributes["endDate"]

        result["thumbnail"] = attributes.get("posterImage", {}).get("original")

        return result

    except Exception:
        raise WebAPIInvalidResponse(service="kitsu.io")


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

        response_content = await search(ctx.bot.session, url, params)
        result = generate_parsed_result(response_content, request_type)

        title = f"{result['title_english']} - {result['title_romaji']}"
        url = result["url"]
        description = result["description"]

        embed = discord.Embed(title=title, url=url, description=description)

        for name, item in result["fields"].items():
            embed.add_field(name=name, value=item)

        embed.set_thumbnail(url=result["thumbnail"])

        await ctx.send(embed=embed)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(KitsuIO())
