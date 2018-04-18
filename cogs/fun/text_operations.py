#!/usr/bin/env python3

"""Commands that invoke random things, part 1."""

import discord
from discord.ext import commands

NUMBER_NAMES = {
    "0": "zero",
    "1": "one",
    "2": "two",
    "3": "three",
    "4": "four",
    "5": "five",
    "6": "six",
    "7": "seven",
    "8": "eight",
    "9": "nine"
}


def to_emojis(string):
    """Convert a string to Discord emojis."""
    memeified_string_list = []
    for character in string:
        if ord(character.lower()) in range(97, 123):
            memeified_string_list.append(f":regional_indicator_{character.lower()}:")
        elif character.isdigit():
            memeified_string_list.append(f":{NUMBER_NAMES[character]}:")
        elif character == "!":
            memeified_string_list.append(f":grey_exclamation:")
        elif character == "?":
            memeified_string_list.append(f":grey_question:")
        elif character == " ":
            memeified_string_list.append(character)
    return " ".join(memeified_string_list)


class Text:
    """Commands that perform text operations."""

    @commands.command(aliases=["memetext"])
    @commands.cooldown(6, 12)
    async def emojify(self, ctx, *, text):
        """Convert text into emoji."""
        text = to_emojis(text)
        await ctx.send(text)

    @commands.command()
    @commands.cooldown(6, 12)
    async def reverse(self, ctx, *, text):
        """Reverse a given text input."""
        text = text[::-1]
        embed = discord.Embed()
        embed.description = text[:800]
        embed.set_footer(text=f"Reversed text requested by {str(ctx.author)}")
        await ctx.send(embed=embed)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Text())
