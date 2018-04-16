#!/usr/bin/env python3

"""This cog contains a Wikipedia query command."""

import urllib.parse

import async_timeout
import discord
from discord.ext import commands

from k2.exceptions import WebAPIInvalidResponse, WebAPINoResultsFound, WebAPIUnreachable

BASE_URL_WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php?{0}"


def generate_search_url(query):
    """Given a query, generate a search URL for Wikipedia's API."""
    params = urllib.parse.urlencode({"action": "opensearch", "search": query})
    url = BASE_URL_WIKIPEDIA_API.format(params)
    return url


async def search(session, url):
    """Given a ClientSession and URL, query the URL and return its response content as a JSON."""
    async with async_timeout.timeout(10):
        async with session.get(url) as response:
            if response.status == 200:
                try:
                    response_content = await response.json()
                except Exception:
                    raise WebAPIInvalidResponse(service="Wikipedia")
            else:
                raise WebAPIUnreachable(service="Wikipedia")

    return response_content


def generate_parsed_results(response_content):
    """Given response content from Wikipedia, parse content into a more easily readable form."""
    try:
        if not response_content[1]:
            raise WebAPINoResultsFound(message="No results found.")

        results = []

        for index in range(0, min(3, len(response_content[1]))):
            result = {
                "title": response_content[1][index],
                "description": response_content[2][index],
                "url": response_content[3][index]
            }
            results.append(result)

        return results

    except Exception:
        raise WebAPIInvalidResponse(service="Wikipedia")


class Wikipedia:
    """Wikipedia command."""

    @commands.command(aliases=["wikipedia"])
    @commands.cooldown(6, 12)
    async def wiki(self, ctx, *, query: str):
        """Search Wikipedia.

        * query - A string to be used in the search criteria.
        """
        url = generate_search_url(query)
        response_content = await search(ctx.bot.session, url)
        results = generate_parsed_results(response_content)

        embed = discord.Embed()
        for result in results:
            description = f"{result['url']}\n{result['description']}"
            embed.add_field(name=result['title'], value=description, inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Wikipedia())
