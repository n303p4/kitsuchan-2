#!/usr/bin/env python3

"""MyAnimeList commands."""

import urllib.parse

import aiohttp
import discord
from discord.ext import commands
import html2text
from bs4 import BeautifulSoup

BASE_URL_MYANIMELIST_SEARCH = "https://myanimelist.net/api/{0}/search.xml?q={1}"
BASE_URL_MYANIMELIST = "https://myanimelist.net/{0}/{1}"


async def _mal_fetch(session, kind, query, username, password):
    """Returns a bs4 tag or a string.

    session is an aiohttp.ClientSession
    kind should be either anime or manga
    query is self-explanatory
    username is self-explanatory
    password is self-explanatory
    """

    auth = aiohttp.BasicAuth(username, password)
    query = urllib.parse.quote(query)
    url = BASE_URL_MYANIMELIST_SEARCH.format(kind, query)

    try:  # This is gross, but MAL doesn't respond nicely.
        async with session.request("GET", url, auth=auth) as response:
            if response.status == 200:
                xml = await response.text()

                soup = BeautifulSoup(xml)
                entry = soup.find("entry")

                return entry
            else:
                message = "Could not reach MyAnimeList. x.x"
                return message

    except aiohttp.ClientResponseError:
        message = ("No results found. Make sure you use spaces (e.g. "
                   "`one piece`, not `onepiece`). Also make sure to spell things right.")
        return message


def _handle_anime(entry):
    embed = discord.Embed(title=entry.title.string)
    embed.url = BASE_URL_MYANIMELIST.format("anime", entry.id.string)
    embed.add_field(name="ID", value=entry.id.string)
    embed.add_field(name="Synonyms", value=entry.synonyms.string)
    embed.add_field(name="Episodes", value=entry.episodes.string)
    embed.add_field(name="Score", value=entry.score.string)
    embed.add_field(name="Type", value=entry.type.string)
    embed.add_field(name="Status", value=entry.status.string)
    embed.add_field(name="Start date", value=entry.start_date.string)
    embed.add_field(name="End date", value=entry.end_date.string)
    embed.description = html2text.html2text(entry.synopsis.string)
    return embed


def _handle_manga(entry):
    embed = discord.Embed(title=entry.title.string)
    embed.url = BASE_URL_MYANIMELIST.format("manga", entry.id.string)
    embed.add_field(name="ID", value=entry.id.string)
    embed.add_field(name="Synonyms", value=entry.synonyms.string)
    embed.add_field(name="Chapters", value=entry.chapters.string)
    embed.add_field(name="Volumes", value=entry.volumes.string)
    embed.add_field(name="Score", value=entry.score.string)
    embed.add_field(name="Type", value=entry.type.string)
    embed.add_field(name="Status", value=entry.status.string)
    embed.add_field(name="Start date", value=entry.start_date.string)
    embed.add_field(name="End date", value=entry.end_date.string)
    embed.description = html2text.html2text(entry.synopsis.string)
    return embed


class MyAnimeList:
    """MyAnimeList lookup commands."""

    @commands.group(invoke_without_command=True)
    @commands.cooldown(6, 12)
    async def mal(self, ctx):
        await ctx.send("Please specify either `anime` or `manga`. Use `help` if you're unsure.")

    @mal.command()
    @commands.cooldown(6, 12)
    async def manga(self, ctx, *, query):
        """Search for manga."""
        username = ctx.bot.config.get("myanimelist_username")
        password = ctx.bot.config.get("myanimelist_password")
        if not username or not password:
            await ctx.send("No username and/or password was found in the configuration.")
            return
        result = await _mal_fetch(ctx.bot.session, "manga", query, username, password)
        if not isinstance(result, str):
            embed = _handle_manga(result)
            await ctx.send(embed=embed)
        else:
            await ctx.send(result)

    @mal.command()
    @commands.cooldown(6, 12)
    async def anime(self, ctx, *, query):
        """Search for anime."""
        username = ctx.bot.config.get("myanimelist_username")
        password = ctx.bot.config.get("myanimelist_password")
        if not username or not password:
            await ctx.send("No username and/or password was found in the configuration.")
            return
        result = await _mal_fetch(ctx.bot.session, "anime", query, username, password)
        if not isinstance(result, str):
            embed = _handle_anime(result)
            await ctx.send(embed=embed)
        else:
            await ctx.send(result)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(MyAnimeList())
