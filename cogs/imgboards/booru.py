#!/usr/bin/env python3
# pylint: disable=C0103

"""Imageboard lookup commands."""

import re
import random
import urllib.parse

import asks
from bs4 import BeautifulSoup
from curious.commands.context import Context
from curious.commands.decorators import command
from curious.commands.plugin import Plugin
from curious.dataclasses.embed import Embed

systemrandom = random.SystemRandom()

BASE_URLS = {"safebooru": {"api": "https://safebooru.org/index.php?{0}",
                           "post": "https://safebooru.org/index.php?page=post&s=view&id={0}"}}

MAX_LENGTH_TAGS = 200
TAGS_BLACKLIST = ["loli", "shota", "lolicon", "shotacon", "scat"]


async def _booru(base_url_api: str, tags: str = "", blacklist: list = None):
    """Generic helper command that can handle most 'booru-type sites.

    * site - The site to check.
    * tags - A list of tags to be used in the search criteria.
    """
    if not blacklist:
        blacklist = TAGS_BLACKLIST
    for tag in blacklist:
        tags += f" -{tag}"
    params = urllib.parse.urlencode({"page": "dapi", "s": "post", "q": "index", "tags": tags})
    url = base_url_api.format(params)
    response = await asks.get(url)
    if response.status_code == 200:
        xml = response.content
        soup = BeautifulSoup(xml, "lxml")
        posts = soup.find_all("post")
        if not posts:
            return ("No results found. Make sure you're using "
                    "standard booru-type tags, such as "
                    "fox_ears or red_hair.")
        post = systemrandom.choice(posts)
        return post
    else:
        message = "Could not reach site; please wait and try again. x.x"
        return message


def _process_post(post, base_url_post: str, max_length_tags: int = MAX_LENGTH_TAGS):
    if re.match("http(s?):\/\/.+", post['sample_url']):
        sample_url = post['sample_url']
    else:
        sample_url = f"https:{post['sample_url']}"
    post_url = base_url_post.format(post["id"])
    embed = Embed(title=post["id"])
    embed.url = post_url
    embed.description = f"[Full-size image](https:{post['file_url']})"
    embed.set_image(image_url=sample_url)
    embed.set_footer(text=post["tags"][:max_length_tags])
    return embed


class Booru(Plugin):
    """Imageboard lookup commands."""

    @command(aliases=["meido"])
    async def maid(self, ctx: Context, *, tags=""):
        """Find a random maid. Optional tags."""
        result = await _booru(BASE_URLS["safebooru"]["api"], f"maid {tags}")
        if isinstance(result, str):
            await ctx.channel.messages.send(result)
        else:
            embed = _process_post(result, BASE_URLS["safebooru"]["post"])
            await ctx.channel.messages.send(embed=embed)

    @command(aliases=["animememe"])
    async def animeme(self, ctx: Context, *, tags=""):
        """Find a random anime meme. Optional tags."""
        result = await _booru(BASE_URLS["safebooru"]["api"], f"meme {tags}")
        if isinstance(result, str):
            await ctx.channel.messages.send(result)
        else:
            embed = _process_post(result, BASE_URLS["safebooru"]["post"])
            await ctx.channel.messages.send(embed=embed)

    @command(name=":<")
    async def colonlessthan(self, ctx: Context, *, tags=""):
        """:<"""
        result = await _booru(BASE_URLS["safebooru"]["api"], f":< {tags}")
        if isinstance(result, str):
            await ctx.channel.messages.send(result)
        else:
            embed = _process_post(result, BASE_URLS["safebooru"]["post"])
            await ctx.channel.messages.send(embed=embed)

    @command(aliases=["sbooru", "sb"])
    async def safebooru(self, ctx: Context, *, tags=""):
        """Fetch a random image from Safebooru. Tags accepted.

        * tags - A list of tags to be used in the search criteria.

        This command accepts common imageboard tags and keywords.
        See http://safebooru.org/index.php?page=help&topic=cheatsheet for more details.
        """
        result = await _booru(BASE_URLS["safebooru"]["api"], tags)
        if isinstance(result, str):
            await ctx.channel.messages.send(result)
        else:
            embed = _process_post(result, BASE_URLS["safebooru"]["post"])
            await ctx.channel.messages.send(embed=embed)
