#!/usr/bin/env python3

"""This extension sets the bot's playing status."""

import discord


def setup(bot):
    """Sets up the extension."""

    @bot.listen("on_ready")
    async def when_ready():
        """Conduct preparations once the bot is ready to go."""

        prefix_choice = bot.config.get('prefix', f'@{bot.user.name}')
        if len(prefix_choice) > 1:  # No space used for single-character prefixes.
            prefix_choice += " "
        name = f"Type {prefix_choice}help for help!"
        game = discord.Game(name=name)

        await bot.change_presence(status=discord.Status.online, activity=game)
