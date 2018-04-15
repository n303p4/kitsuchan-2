#!/usr/bin/env python3

"""This cog contains a Wikipedia query command."""

import urllib.parse

import discord
from discord.ext import commands

BASE_URL_WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php?{0}"


def generate_search_url_wikipedia(query):
    params = urllib.parse.urlencode({"action": "opensearch", "search": query})
    url = BASE_URL_WIKIPEDIA_API.format(params)
    return url


async def search_wikipedia(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            response_content = await response.json()
        else:
            return "Couldn't reach Wikipedia. x.x"
    if not response_content[1]:
        return "No results found. :<"
    return response_content


def generate_parsed_results_wikipedia(response_content):
    results = []
    for index in range(0, min(3, len(response_content[1]))):
        result = {
            "title": response_content[1][index],
            "description": response_content[2][index],
            "url": response_content[3][index]
        }
        results.append(result)
    return results


class Wikipedia:
    """Wikipedia command."""

    @commands.command(aliases=["wikipedia"])
    @commands.cooldown(6, 12)
    async def wiki(self, ctx, *, query: str):
        """Search Wikipedia.

        * query - A string to be used in the search criteria.
        """
        url = generate_search_url_wikipedia(query)
        response_content = await search_wikipedia(ctx.bot.session, url)
        if isinstance(response_content, list):
            results = generate_parsed_results_wikipedia(response_content)
            embed = discord.Embed()
            for result in results:
                description = f"{result['url']}\n{result['description']}"
                embed.add_field(name=result['title'], value=description, inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(response_content)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Wikipedia())
