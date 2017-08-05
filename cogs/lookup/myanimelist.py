#!/usr/bin/env python3

"""MyAnimeList commands."""

import random
import urllib.parse

import aiohttp
from discord.ext import commands
import html2text
from bs4 import BeautifulSoup

systemrandom = random.SystemRandom()

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


def _handle_anime(formatter, entry):
    message = [
        formatter.bold(entry.title.string),
        formatter.no_embed_link(BASE_URL_MYANIMELIST.format("anime", entry.id.string)),
        formatter.bold("ID: ") + entry.id.string,
        formatter.bold("Synonyms: ") + entry.synonyms.string,
        formatter.bold("Episodes: ") + entry.synonyms.string,
        formatter.bold("Score: ") + entry.score.string,
        formatter.bold("Type: ") + entry.type.string,
        formatter.bold("Status: ") + entry.status.string,
        formatter.bold("Start date: ") + entry.start_date.string,
        formatter.bold("End date: ") + entry.end_date.string,
        html2text.html2text(entry.synopsis.string)
    ]
    return "\n".join(message)


def _handle_manga(formatter, entry):
    message = [
        formatter.bold(entry.title.string),
        formatter.no_embed_link(BASE_URL_MYANIMELIST.format("manga", entry.id.string)),
        formatter.bold("ID: ") + entry.id.string,
        formatter.bold("Synonyms: ") + entry.synonyms.string,
        formatter.bold("Chapters: ") + entry.chapters.string,
        formatter.bold("Volumes: ") + entry.volumes.string,
        formatter.bold("Score: ") + entry.score.string,
        formatter.bold("Type: ") + entry.type.string,
        formatter.bold("Status: ") + entry.status.string,
        formatter.bold("Start date: ") + entry.start_date.string,
        formatter.bold("End date: ") + entry.end_date.string,
        html2text.html2text(entry.synopsis.string)
    ]
    return "\n".join(message)


@commands.cooldown(6, 12)
@commands.command()
async def manga(ctx, query, *args):
    """Search for manga."""
    query += " ".join(args)
    username = ctx.bot.config.get("myanimelist_username")
    password = ctx.bot.config.get("myanimelist_password")
    if not username or not password:
        await ctx.send("No username and/or password was found in the configuration.")
        return
    result = await _mal_fetch(ctx.bot.session, "manga", query, username, password)
    if not isinstance(result, str):
        result = _handle_manga(ctx.formatter, result)
    await ctx.send(result)


@commands.cooldown(6, 12)
@commands.command()
async def anime(ctx, query, *args):
    """Search for anime."""
    query += " ".join(args)
    username = ctx.bot.config.get("myanimelist_username")
    password = ctx.bot.config.get("myanimelist_password")
    if not username or not password:
        await ctx.send("No username and/or password was found in the configuration.")
        return
    result = await _mal_fetch(ctx.bot.session, "anime", query, username, password)
    if not isinstance(result, str):
        result = _handle_anime(ctx.formatter, result)
    await ctx.send(result)
