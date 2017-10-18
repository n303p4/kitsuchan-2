#!/usr/bin/env python3
# pylint: disable=C0103

"""Contains a cog for various weeb reaction commands."""
import random

import discord
from discord.ext import commands

from k2 import helpers

systemrandom = random.SystemRandom()

BASE_URL_API_TYPE = "https://api.weeb.sh/images/random?type={0}"
BASE_URL_API_TAG = "https://api.weeb.sh/images/random?tags={0}"
EMOJIS_KILL = (":gun:", ":knife:", ":eggplant:", ":bear:", ":fox:", ":wolf:", ":snake:",
               ":broken_heart:", ":crossed_swords:", ":fire:")


async def _generate_message(ctx, kind: str = None, user: str = None):
    """Generate a message based on the user."""
    user = await helpers.member_by_substring(ctx, user)
    if not kind or not user:
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


async def _rra(ctx, kind: str, message: str = "", usetag: bool = False):
    """A helper function that grabs an image and posts it in response to a user.

    * kind - The type of image to retrieve.
    * user - The member to mention in the command.
    """
    if usetag:
        url = BASE_URL_API_TAG.format(kind)
    else:
        url = BASE_URL_API_TYPE.format(kind)
    async with ctx.bot.session.get(url, headers={
        'Authorization': f"Wolke {ctx.bot.config.get('weebsh_token')}"}) as response:
        if response.status == 200:
            data = await response.json()
            url_image = data['url']
            embed = discord.Embed(title=message)
            embed.set_image(url=url_image)
            embed.set_footer(text="Powered by weeb.sh")
            await ctx.send(embed=embed)
        else:
            message = "Could not retrieve image. :("
            await ctx.send(message)


async def _send_image(ctx, url_image, message: str = ""):
    """A helper function that creates an embed with an image and sends it off."""
    if isinstance(url_image, (tuple, list)):
        url_image = systemrandom.choice(url_image)
    embed = discord.Embed(title=message)
    embed.set_image(url=url_image)
    await ctx.send(embed=embed)


class Ram:
    """Weeb reaction commands."""

    @commands.command(aliases=["chomp"])
    @commands.cooldown(6, 12)
    async def bite(self, ctx, *, user: str):
        """Bite a user!

        * user - the user to be bitten.
        """
        # custom message here since it sounds weird to use bite
        message = f"**{user.display_name}**, you got bitten by **{ctx.author.display_name}!**"
        await _rra(ctx, "bite", message)

    @commands.command(aliases=["cuddles", "snuggle", "snuggles"])
    @commands.cooldown(6, 12)
    async def cuddle(self, ctx, *, user: str):
        """Cuddle a user!

        * user - The user to be cuddled.
        """
        message = await _generate_message(ctx, "cuddle", user)
        await _rra(ctx, "cuddle", message)

    @commands.command()
    @commands.cooldown(6, 12)
    async def hug(self, ctx, *, user: str):
        """Hug a user!

        * user - The user to be hugged.
        """
        message = await _generate_message(ctx, "hug", user)
        await _rra(ctx, "hug", message)

    @commands.command(aliases=["fdesk"])
    @commands.cooldown(6, 12)
    async def facedesk(self, ctx):
        """Hit your face on the desk!"""
        await _rra(ctx, "facedesk","", True)

    @commands.command()
    @commands.cooldown(6, 12)
    async def kiss(self, ctx, *, user: str):
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
    async def lick(self, ctx, *, user: str):
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
        await _rra(ctx, "neko", f"{ctx.invoked_with.capitalize()}~")

    @commands.command()
    @commands.cooldown(6, 12)
    async def owo(self, ctx):
        """owo"""
        await _rra(ctx, "owo")

    @commands.command(aliases=["headpat", "pet"])
    @commands.cooldown(6, 12)
    async def pat(self, ctx, *, user: str):
        """Pat a user!

        * user - The user to be patted.
        """
        message = await _generate_message(ctx, "pat", user)
        await _rra(ctx, "pat", message)

    @commands.command()
    @commands.cooldown(6, 12)
    async def poke(self, ctx, *, user: str):
        """Poke someone

        * user - the user to be poked.
        """
        message = await _generate_message(ctx, "poke", user)
        await _rra(ctx, "poke", message)

    @commands.command()
    @commands.cooldown(6, 12)
    async def pout(self, ctx):
        """Pout!"""
        await _rra(ctx, "pout")

    @commands.command()
    @commands.cooldown(6, 12)
    async def slap(self, ctx, *, user: str):
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
    async def stare(self, ctx, *, user: str):
        """Stare at a user!

        * user - The user to be stared at.
        """
        message = await _generate_message(ctx, "stare", user)
        await _rra(ctx, "stare", message)

    @commands.command()
    @commands.cooldown(6, 12)
    async def tickle(self, ctx, *, user: str):
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
