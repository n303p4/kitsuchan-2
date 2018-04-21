#!/usr/bin/env python3

import subprocess

from discord.ext import commands


class Evaluation:
    """Commands that evaluate expressions."""

    @commands.command()
    @commands.is_owner()
    async def sh(self, ctx, *, command):
        """Execute a system command. Bot owner only."""
        command = command.split(" ")
        process = subprocess.Popen(command,
                                   universal_newlines=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        try:
            output, errors = process.communicate(timeout=8)
            output = output.split("\n")
            process.terminate()
        except subprocess.TimeoutExpired:
            process.kill()
            output = ["Command timed out. x.x"]
        paginator = commands.Paginator(prefix="```bash")
        for line in output:
            paginator.add_line(line)
        for page in paginator.pages:
            await ctx.send(page)

    @commands.command(name="exec")
    @commands.is_owner()
    async def _exec(self, ctx, *, code):
        """Execute arbitrary Python code. Bot owner only."""
        if code.startswith("```py\n"):
            code = code[6:]
        elif code.startswith("```"):
            code = code[3:]

        if code.endswith("```"):
            code = code[:-3]

        variables = {"ctx": ctx}
        exec(code, {}, variables)
        paginator = commands.Paginator()
        for key, value in variables.items():
            paginator.add_line(f"{type(value).__name__} {key}: {value}")
        for page in paginator.pages:
            await ctx.send(page)


def setup(bot):
    """Sets up the cog."""
    bot.add_cog(Evaluation())
