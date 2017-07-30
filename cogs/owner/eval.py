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

    async def _geval(self, ctx, expression, type_=None):
        """Evaluate an expression."""
        try:
            if type_ == "await":
                output = await eval(expression)
            elif type_ == "exec":
                output = exec(expression)
            else:
                output = eval(expression)
            output = str(output)
        except Exception as error:
            output = f"x.x An error has occurred: {error}"
        paginator = commands.Paginator(prefix="```py", max_size=500)
        for index in range(0, len(output), 490):
            paginator.add_line(output[index:index+490])
        message = await ctx.send(paginator.pages[0])
        await ctx.bot.add_pager(message, paginator.pages, author_id=ctx.author.id)

    @commands.group(name="eval", invoke_without_command=True)
    @commands.is_owner()
    async def _eval(self, ctx, *, expression):
        """Evaluate a Python expression. Bot owner only."""
        await self._geval(ctx, expression)

    @_eval.command(name="await")
    @commands.is_owner()
    async def _await(self, ctx, *, expression):
        """Evaluate a Python expression as an await. Bot owner only."""
        await self._geval(ctx, expression, type_="await")

    @commands.group(name="exec", invoke_without_command=True)
    @commands.is_owner()
    async def _exec(self, ctx, *, expression):
        """Execute a Python expression. Bot owner only."""
        await self._geval(ctx, expression, type_="exec")


def setup(bot):
    """Sets up the cog."""
    bot.add_cog(Evaluation())
