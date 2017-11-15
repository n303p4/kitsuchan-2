#!/usr/bin/env python3

"""A cog containing a command that generates a meme out of someone."""

import urllib.parse

import discord
from discord.ext import commands

BASE_URL_MEMEGEN = "https://memegen.link/custom/{0}/{1}.jpg?alt={2}"


class Memes:
    """A cog that contains a meme generator."""

    def __init__(self):
        self.footer_text = "Powered by memegen.link"

    @commands.command()
    @commands.cooldown(6, 12)
    async def meme(self, ctx, *, pair_of_lines: str):
        """Generates a meme of an image with a top line and a bottom line.

        If you attach an image when you issue the command, then the bot will use that image.
        Otherwise, it attempts to use the last image it can find in the last 100 chat messages.

        This secondary behavior is useful because you can immediately follow up a previous image
        command with this command. For example, following up an avatar command to generate a
        meme of someone's avatar.

        Example usage:

        kit meme I am | a meme
        """
        image_url = None
        async for message in ctx.channel.history():
            if message.embeds:
                for embed in reversed(message.embeds):
                    if embed.type == "image":
                        image_url = embed.url
                        break
                    elif (embed.type == "rich" and
                            embed.image is not discord.Embed.Empty and
                            embed.footer.text != self.footer_text):
                        image_url = embed.image.url
                        break
            elif message.attachments:
                for attachment in message.attachments:
                    if attachment.height:
                        image_url = attachment.url
                        break
            if image_url:
                break
        if not image_url:
            await ctx.send(("No images found in recent chat history. "
                            "You may upload an image as an attachment."
                            "Use quotation marks or underscores if you need to use spaces."))
            return
        lines = pair_of_lines.split("|")
        if len(lines) < 2:
            await ctx.send("Please separate the top and bottom lines with a `|`")
            return
        top_line = lines[0].strip().replace(" ", "_")
        bottom_line = lines[1].strip().replace(" ", "_")
        url = BASE_URL_MEMEGEN.format(urllib.parse.quote(top_line), urllib.parse.quote(bottom_line),
                                      image_url)
        print(url)
        embed = discord.Embed(title="Image link")
        embed.url = url
        embed.set_image(url=url)
        embed.set_footer(text=self.footer_text)
        await ctx.send(embed=embed)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Memes())
