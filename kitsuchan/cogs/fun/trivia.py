#!/usr/bin/env python3
# pylint: disable=C0103

"""Trivia module with a trivia command."""

import html
import random

import discord
from discord.ext import commands

from k2.helpers import input_number

URL_NUMBERS_API = "http://numbersapi.com/{0}/{1}"
OPTIONS_NUMBERS_API = ["math", "trivia"]
URL_TRIVIA_API = "https://opentdb.com/api.php?amount=1"

systemrandom = random.SystemRandom()


class Trivia:
    """Trivia commands."""

    @commands.command(aliases=["numberfact", "number"])
    @commands.cooldown(12, 12, commands.BucketType.channel)
    async def numfact(self, ctx, number: int):
        """Display a random fact about a number."""
        kind = systemrandom.choice(OPTIONS_NUMBERS_API)
        url = URL_NUMBERS_API.format(number, kind)
        async with ctx.bot.session.get(url) as response:
            if response.status == 200:
                data = await response.text()
                await ctx.send(data)
            else:
                await ctx.send("Could not fetch fact. :<")

    @commands.command()
    @commands.cooldown(6, 12, commands.BucketType.channel)
    async def trivia(self, ctx):
        """Ask a random trivia question."""
        async with ctx.bot.session.get(URL_TRIVIA_API) as response:
            if response.status == 200:
                data = await response.json()

                trivia = data["results"][0]

                correct_answer = html.unescape(trivia["correct_answer"])
                incorrect_answers = []
                for answer in trivia["incorrect_answers"]:
                    incorrect_answers.append(html.unescape(answer))

                choices = [correct_answer] + incorrect_answers

                systemrandom.shuffle(choices)

                embed = discord.Embed()
                embed.title = html.unescape(trivia["category"])
                embed.description = html.unescape(trivia["question"])

                difficulty = html.unescape(trivia["difficulty"]).capitalize()
                footer_text = f"Powered by Open Trivia DB | Difficulty: {difficulty}"

                embed.set_footer(text=footer_text)

                paginator = commands.Paginator(prefix="```markdown")

                for index, value in enumerate(choices):
                    paginator.add_line(f"{index+1}. {value}")

                embed.add_field(name="Options", value=paginator.pages[0])

                await ctx.send(ctx.author.mention, embed=embed)
                choice = await input_number(ctx, "Answer by number in 15 seconds.",
                                            timeout=15, min_value=1,
                                            max_value=len(choices))

                if choices[choice-1] == correct_answer:
                    await ctx.send("Correct! :3")

                else:
                    await ctx.send(f"Nope, the correct answer is {correct_answer}. :<")

            else:
                await ctx.send("Could not fetch trivia. :<")


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Trivia())
