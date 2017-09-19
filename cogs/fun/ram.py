#!/usr/bin/env python3
# pylint: disable=C0103

"""Contains a cog for various weeb reaction commands."""

import random

import discord
from discord.ext import commands

systemrandom = random.SystemRandom()

BASE_URL_API = "https://rra.ram.moe/i/r?type={0}"
BASE_URL_IMAGE = "https://cdn.ram.moe{0[path]}"

EMOJIS_KILL = (":gun:", ":knife:", ":eggplant:", ":bear:", ":fox:", ":wolf:", ":snake:",
               ":broken_heart:", ":crossed_swords:", ":fire:")


async def _generate_message(ctx, kind: str=None, user: str=discord.Member):
    """Generate a message based on the user."""
    if not kind:
        message = ""
    elif user.id == ctx.bot.user.id:
        message = f"Aw, thank you. Here, have one back. :3"
    elif user.id == ctx.author.id:
        message = systemrandom.choice(("Okay. :3",
                                       f"Sorry to see you're alone, have a {kind} anyway. :<",
                                       f"I'll {kind} your face alright. :3",
                                       ":<"))
    else:
        message = f"**{user.display_name}**, you got a {kind} from **{ctx.author.display_name}!**"
    return message


async def _rra(ctx, kind: str, message: str=""):
    """A helper function that grabs an image and posts it in response to a user.

    * kind - The type of image to retrieve.
    * user - The member to mention in the command.
    """
    url = BASE_URL_API.format(kind)
    async with ctx.bot.session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            url_image = BASE_URL_IMAGE.format(data).replace("i/", "")
            embed = discord.Embed(title=message)
            embed.set_image(url=url_image)
            embed.set_footer(text="Powered by ram.moe")
            await ctx.send(embed=embed)
        else:
            message = "Could not retrieve image. :("
            await ctx.send(message)


async def _send_image(ctx, url_image, message: str=""):
    """A helper function that creates an embed with an image and sends it off."""
    if isinstance(url_image, (tuple, list)):
        url_image = systemrandom.choice(url_image)
    embed = discord.Embed(title=message)
    embed.set_image(url=url_image)
    await ctx.send(embed=embed)


class Ram:
    """Weeb reaction commands."""

    @commands.command(aliases=["cuddles", "snuggle", "snuggles"])
    @commands.cooldown(6, 12)
    async def cuddle(self, ctx, *, user: discord.Member):
        """Cuddle a user!

        * user - The user to be cuddled.
        """
        message = await _generate_message(ctx, "cuddle", user)
        await _rra(ctx, "cuddle", message)

    @commands.command()
    @commands.cooldown(6, 12)
    async def hug(self, ctx, *, user: discord.Member):
        """Hug a user!

        * user - The user to be hugged.
        """
        message = await _generate_message(ctx, "hug", user)
        await _rra(ctx, "hug", message)

    @commands.command()
    @commands.cooldown(6, 12)
    async def kiss(self, ctx, *, user: discord.Member):
        """Kiss a user!

        * user - The user to be kissed.
        """
        message = await _generate_message(ctx, "kiss", user)
        await _rra(ctx, "kiss", message)

    @commands.command(aliases=["2lewd", "2lewd4me"])
    @commands.cooldown(6, 12)
    async def lewd(self, ctx):
        """Lewd!"""
        await _rra(ctx, "lewd")

    @commands.command()
    @commands.cooldown(6, 12)
    async def lick(self, ctx, *, user: discord.Member):
        """Lick a user!

        * user - The user to be licked.
        """
        message = await _generate_message(ctx, "lick", user)
        await _rra(ctx, "lick", message)

    @commands.command()
    @commands.cooldown(6, 12)
    async def nom(self, ctx):
        """Nom!"""
        await _rra(ctx, "nom")

    @commands.command(aliases=['nya', 'meow'])
    @commands.cooldown(6, 12)
    async def nyan(self, ctx):
        """Nyan!"""
        await _rra(ctx, "nyan", f"{ctx.invoked_with.capitalize()}~")

    @commands.command()
    @commands.cooldown(6, 12)
    async def owo(self, ctx):
        """owo"""
        await _rra(ctx, "owo")

    @commands.command(aliases=["headpat", "pet"])
    @commands.cooldown(6, 12)
    async def pat(self, ctx, *, user: discord.Member):
        """Pat a user!

        * user - The user to be patted.
        """
        message = await _generate_message(ctx, "pat", user)
        await _rra(ctx, "pat", message)

    @commands.command()
    @commands.cooldown(6, 12)
    async def pout(self, ctx):
        """Pout!"""
        await _rra(ctx, "pout")

    @commands.command()
    @commands.cooldown(6, 12)
    async def slap(self, ctx, *, user: discord.Member):
        """Slap a user!

        * user - The user to be slapped.
        """
        message = await _generate_message(ctx, "slap", user)
        await _rra(ctx, "slap", message)

    @commands.command()
    @commands.cooldown(6, 12)
    async def smug(self, ctx):
        """Smug!"""
        await _rra(ctx, "smug")

    @commands.command()
    @commands.cooldown(6, 12)
    async def stare(self, ctx, *, user: discord.Member):
        """Stare at a user!

        * user - The user to be stared at.
        """
        message = await _generate_message(ctx, "stare", user)
        await _rra(ctx, "stare", message)

    @commands.command()
    @commands.cooldown(6, 12)
    async def tickle(self, ctx, *, user: discord.Member):
        """Tickle a user!

        * user - The user to be tickled.
        """
        message = await _generate_message(ctx, "tickle", user)
        await _rra(ctx, "tickle", message)

    @commands.command()
    @commands.cooldown(6, 12)
    async def triggered(self, ctx):
        """Triggered!"""
        await _rra(ctx, "triggered")


def setup(bot):
    """Setup function for reaction images."""
    bot.add_cog(Ram())
