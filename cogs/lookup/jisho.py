#!/usr/bin/env python3

"""jisho.org query command."""

import urllib.parse

import discord
from discord.ext import commands

from k2.helpers import query_web_api
from k2.exceptions import WebAPIInvalidResponse, WebAPINoResultsFound

BASE_URL_JISHO_API = "http://jisho.org/api/v1/search/words?{0}"


def generate_search_url(query):
    """Given a query, generate a search URL for jisho.org's API."""
    params = urllib.parse.urlencode({"keyword": query})
    url = BASE_URL_JISHO_API.format(params)
    return url


def generate_parsed_result(response_content):
    """Given response content from jisho.org, parse content into a more easily readable form."""
    try:
        if not response_content.get("data"):
            raise WebAPINoResultsFound(message="No result found.")

        japanese = response_content["data"][0]["japanese"][0]
        sense = response_content["data"][0]["senses"][0]
        english_string = ", ".join(sense["english_definitions"])

        result = {
            "kanji": str(japanese.get("word")),
            "kana": str(japanese.get("reading")),
            "english": english_string
        }

        return result

    except Exception:
        raise WebAPIInvalidResponse(service="jisho.org")


class Jisho:
    """A Japanese translation command."""

    @commands.command(aliases=["jp"])
    @commands.cooldown(6, 12)
    async def jisho(self, ctx, query, *args):
        """Translate a word into Japanese.

        Example usage:
        jisho test
        """
        query = f"{query} {' '.join(args)}"

        url = generate_search_url(query)
        response_content = await query_web_api(ctx.bot.session, url, service="jisho.org")
        result = generate_parsed_result(response_content)

        embed = discord.Embed()
        embed.add_field(name="Kanji", value=result["kanji"])
        embed.add_field(name="Kana", value=result["kana"])
        embed.add_field(name="English", value=result["english"])

        await ctx.send(embed=embed)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Jisho())
