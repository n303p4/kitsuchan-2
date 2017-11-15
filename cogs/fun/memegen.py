#!/usr/bin/env python3

"""A cog containing a command that generates a meme out of someone."""

import discord
from discord.ext import commands

from k2 import helpers

BASE_URL_MEMEGEN = "https://memegen.link/custom/{0}/{1}.jpg?alt={2}"


class Memes:
    """A cog that contains a meme generator."""

    @commands.command(aliases=["usermeme", "um"])
    @commands.cooldown(6, 12)
    async def meme(self, ctx, *, lines: str):
        """Generates a meme of an image.

        If you attach an image when you issue the command, then the bot will use that image.
        Otherwise, it attempts to use the last image it can find in the last 100 chat messages.

        Be sure to separate your lines of text with a |.

        Example usage:

        kit meme I am | a meme
        """
        image_url = None
        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                if attachment.height:
                    image_url = attachment.url
                    break
        else:
            async for message in await ctx.channel.history():
                if message.embeds:
                    for embed in reversed(message.embeds):
                        if embed.type == "image":
                            image_url = embed.url
                            break
                        elif embed.type == "rich" and embed.image is not discord.Embed.Empty:
                            image_url = embed.image.url
                            break
                if image_url:
                    break
            if not image_url:
                await ctx.send(("No images found in recent chat history. "
                                "You may also upload an image as an attachment."))
                return
        lines = lines.split("|")
        if len(lines) < 2:
            await ctx.send("Please split the top and bottom lines with a |.")
            return
        for index, item in enumerate(lines):
            lines[index] = item.strip().replace(" ", "_")
        url = BASE_URL_MEMEGEN.format(lines[0], lines[1], image_url)
        print(url)
        embed = discord.Embed(title="Image link")
        embed.url = url
        embed.set_image(url=url)
        await ctx.send(embed=embed)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Memes())
