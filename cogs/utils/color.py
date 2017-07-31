#!/usr/bin/env python3

"""Contains a cog that fetches colors."""

import colorsys
import random

import discord
from discord.ext import commands
import webcolors

BASE_URL_COLOR_API = "https://api.thegathering.xyz/color/?color={0}"
BASE_URL_TINEYE_MULTICOLR = "https://labs.tineye.com/multicolr/#colors={0};weights=100"
BASE_URL_COLOR_HEX = "http://www.color-hex.com/color/{0}"

systemrandom = random.SystemRandom()


def rgb_to_hsv(red, green, blue):
    """Convert an RGB tuple to an HSV tuple."""
    hue, saturation, value = colorsys.rgb_to_hsv(red/255, green/255, blue/255)
    return int(hue*360), int(saturation*100), int(value*100)


def rgb_to_hls(red, green, blue):
    """Convert an RGB tuple to an HLS tuple."""
    hue, lightness, saturation = colorsys.rgb_to_hls(red/255, green/255, blue/255)
    return int(hue*360), int(lightness*100), int(saturation*100)


class Color:
    """Color command."""

    @commands.command(aliases=["colour"])
    @commands.cooldown(6, 12)
    async def color(self, ctx, *, color: str=None):
        """Display a color. Accepts CSS color names and hex input.

        * color - Either a CSS color or hex input.
        """
        try:
            color = webcolors.name_to_hex(color)
        except (ValueError, AttributeError):
            pass
        try:
            if color:
                color = color.lstrip("#")  # Remove the pound sign.
                color = int(f"0x{color}", 16)
            else:
                color = systemrandom.randint(0, 16777215)
            color = discord.Color(color)
        except ValueError:
            raise commands.UserInputError(("Not a valid color. "
                                           "Color must either be A) in hex format (e.g. `808080`)"
                                           " and between `FFFFFF` and `000000`, or B) A named CSS"
                                           " color (e.g. `red` or `purple`."))

        color_hex_value = "%0.2X%0.2X%0.2X" % (color.r, color.g, color.b)

        embed = discord.Embed()
        embed.colour = color
        image_url = BASE_URL_COLOR_API.format(color_hex_value)
        embed.set_thumbnail(url=image_url)
        color_as_rgb = color.to_rgb()
        color_as_rgba = color_as_rgb + (1.0,)
        embed.add_field(name="RGB", value=f"rgb{color_as_rgb}")
        embed.add_field(name="RGBA", value=f"rgba{color_as_rgba}")
        embed.add_field(name="HSV*", value=f"{rgb_to_hsv(*color_as_rgb)}")
        embed.add_field(name="HLS*", value=f"{rgb_to_hls(*color_as_rgb)}")
        embed.add_field(name="Hex code", value=f"#{color_hex_value}")
        embed.add_field(name="Images",
                        value=BASE_URL_TINEYE_MULTICOLR.format(color_hex_value.lower()))
        embed.add_field(name="Information",
                        value=BASE_URL_COLOR_HEX.format(color_hex_value.lower()))
        embed.add_field(name="Notes",
                        value="* These values may be slightly wrong due to floating point errors.",
                        inline=False)
        embed.set_footer(text="Thumbnail provided by AlexFlipnote's API")
        await ctx.send(embed=embed)


def setup(bot):
    """Sets up the cog."""
    bot.add_cog(Color())
