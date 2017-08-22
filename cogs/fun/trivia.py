#!/usr/bin/env python3

# TODO Audit this code later for cleanup.

import html
import random

import asyncio
import discord
from discord.ext import commands

URL_NUMBERS_API = "http://numbersapi.com/{0}/{1}"
OPTIONS_NUMBERS_API = ["math", "trivia"]
URL_TRIVIA_API = "https://opentdb.com/api.php?amount=1"

systemrandom = random.SystemRandom()


async def input_number(ctx: commands.Context,
                       message: str="Please enter a number within 10 seconds.",
                       *, timeout: int=10, min_value: int=None, max_value: int=None):
    """Number input helper, with timeout.

    * ctx - The context in which the question is being asked.
    * message - Optional messsage that the question should ask.
    * timeout - Timeout, in seconds, before automatically failing. Defaults to 10.
    * min_value - Minimum accepted value for the input. Defaults to None.
    * max_value - Maximum accepted value for the input. Defaults to None.
    """
    await ctx.send(message)

    def check(message):
        """The check function used in bot.wait_for()."""
        if message.author != ctx.message.author or not message.clean_content.isdecimal():
            return False

        number = int(message.clean_content)

        if (min_value and number < min_value) or (max_value and number > max_value):
            return False

        return True

    try:
        message = await ctx.bot.wait_for("message", timeout=timeout, check=check)

    except asyncio.TimeoutError:
        raise commands.UserInputError("Timed out waiting.")

    return int(message.clean_content)


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

                for index in range(len(choices)):
                    paginator.add_line(f"{index+1}. {choices[index]}")

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
