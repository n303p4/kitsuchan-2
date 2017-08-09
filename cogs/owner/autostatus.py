#!/usr/bin/env python3

"""This extension sets the bot's playing status."""

import discord


def setup(bot):
    """Sets up the extension."""

    @bot.listen("on_ready")
    async def when_ready():
        """Conduct preparations once the bot is ready to go."""

        game = discord.Game()
        game.name = f"Type {bot.config.get('prefix', f'@{bot.user.name}')} help for help!"

        await bot.change_presence(game=game)
