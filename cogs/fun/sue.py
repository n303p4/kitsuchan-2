#!/usr/bin/env python3

"""A command that sues someone or something."""

import random
import re

from discord.ext import commands

systemrandom = random.SystemRandom()


class Sue:
    """This command sues somebody!"""

    @commands.command()
    @commands.cooldown(6, 12)
    async def sue(self, ctx, *, target):
        """Sue somebody!

        Example usage:

        * sue
        * sue a person
        """
        conjunctions = " because | for | over "
        parts = [part.strip() for part in re.split(conjunctions, target, 1, re.I)]
        if len(parts) > 1 and parts[1]:
            conjunction = re.search(conjunctions, target, re.I).group(0)
            target = parts[0]
            reason = f"{conjunction}**{parts[1]}**"
        else:
            reason = ""
        if target:
            target = f" {target}"
        amount = f"**${str(systemrandom.randint(100, 1000000))}**"
        message = f"I-I'm going to sue{target} for {amount}{reason}! o.o"
        await ctx.send(message)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Sue())
