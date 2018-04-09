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
            await ctx.send(f"Required parameter `{exc.param}` is missing.")
        elif not isinstance(exc, (commands.CommandNotFound, IsNotHuman)):
            await ctx.send(exc)
