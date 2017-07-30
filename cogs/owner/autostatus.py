#!/usr/bin/env python3

"""
This cog sets the bot's prefix and playing status.
"""

import discord


class AutoStatus:
    """This cog contains no commands."""

    def __init__(self, bot):

        @bot.listen("on_ready")
        async def when_ready():
            """Conduct preparations once the bot is ready to go."""

            game = discord.Game()
            game.name = f"@{bot.user.name} help for help!"

            await bot.change_presence(game=game)


def setup(bot):
    """Sets up the cog."""
    bot.add_cog(AutoStatus(bot))
