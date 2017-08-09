#!/usr/bin/env python3

"""A simple error handling extension. Should work with any discord.ext-based bot."""

from discord.ext import commands


class IsNotHuman(commands.CommandError):
    """Raised if a bot attempts to invoke one of this bot's commands."""
    pass


def setup(bot):
    """Set up the cog."""

    @bot.check
    def is_human(ctx):
        """Prevent the bot from responding to other bots."""
        if ctx.author.bot:
            raise IsNotHuman("User is not human")
        return True

    @bot.listen("on_command_error")
    async def handle_error(ctx, exc):
        """Simple error handler."""
        if isinstance(exc, commands.MissingRequiredArgument):
            param = exc.param.replace("_", " ")
            await ctx.send(f"Please specify a {param} for this command to work.")
        elif not isinstance(exc, (commands.CommandNotFound, IsNotHuman)):
            await ctx.send(exc)
