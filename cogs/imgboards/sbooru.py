#!/usr/bin/env python3

"""Imageboard lookup commands."""

import re
import random
import urllib.parse

from bs4 import BeautifulSoup
import discord
from discord.ext import commands

systemrandom = random.SystemRandom()

BASE_URLS = {"safebooru": {"api": "https://safebooru.org/index.php?{0}",
                           "post": "https://safebooru.org/index.php?page=post&s=view&id={0}"}}

MAX_LENGTH_TAGS = 200
TAGS_BLACKLIST = ["loli", "shota", "lolicon", "shotacon", "scat"]


async def _booru(session, base_url_api: str, tags: str="", blacklist: list=None):
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
    async with session.get(url) as response:
        if response.status == 200:
            xml = await response.text()
            soup = BeautifulSoup(xml)
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


def _process_post(post, base_url_post: str, max_length_tags: int=MAX_LENGTH_TAGS):
    if re.match("http(s?):\/\/.+", post['sample_url']):
        sample_url = post['sample_url']
    else:
        sample_url = f"https:{post['sample_url']}"
    post_url = base_url_post.format(post["id"])
    embed = discord.Embed(title=post_url)
    embed.add_field(name="Full-size image", value=f"https:{post['file_url']}")
    embed.set_image(url=sample_url)
    embed.set_footer(text=post["tags"][:max_length_tags])
    return embed


class Booru:
    """Imageboard lookup commands."""

    @commands.command(aliases=["meido"])
    @commands.cooldown(6, 12)
    async def maid(self, ctx, *, tags):
        """Find a random maid. Optional tags."""
        tags = " ".join(tags)
        result = await _booru(ctx.bot.session, BASE_URLS["safebooru"]["api"], f"maid {tags}")
        if isinstance(result, str):
            await ctx.send(result)
        else:
            embed = _process_post(result, BASE_URLS["safebooru"]["post"])
            await ctx.send(embed=embed)

    @commands.command(aliases=["animememe"])
    @commands.cooldown(6, 12)
    async def animeme(self, ctx, *, tags):
        """Find a random anime meme. Optional tags."""
        tags = " ".join(tags)
        result = await _booru(ctx.bot.session, BASE_URLS["safebooru"]["api"], f"meme {tags}")
        if isinstance(result, str):
            await ctx.send(result)
        else:
            embed = _process_post(result, BASE_URLS["safebooru"]["post"])
            await ctx.send(embed=embed)

    @commands.command(name=":<")
    @commands.cooldown(6, 12)
    async def colonlessthan(self, ctx, *, tags):
        """:<"""
        tags = " ".join(tags)
        result = await _booru(ctx.bot.session, BASE_URLS["safebooru"]["api"], f":< {tags}")
        if isinstance(result, str):
            await ctx.send(result)
        else:
            embed = _process_post(result, BASE_URLS["safebooru"]["post"])
            await ctx.send(embed=embed)

    @commands.command(aliases=["sbooru", "sb"])
    @commands.cooldown(6, 12)
    async def safebooru(self, ctx, *, tags):
        """Fetch a random image from Safebooru. Tags accepted.

        * tags - A list of tags to be used in the search criteria.

        This command accepts common imageboard tags and keywords.
        See http://safebooru.org/index.php?page=help&topic=cheatsheet for more details.
        """
        result = await _booru(ctx.bot.session, BASE_URLS["safebooru"]["api"], tags)
        if isinstance(result, str):
            await ctx.send(result)
        else:
            embed = _process_post(result, BASE_URLS["safebooru"]["post"])
            await ctx.send(embed=embed)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Booru())
