#!/usr/bin/env python3

"""This extension sets the bot's playing status."""

import discord


def setup(bot):
    """Sets up the extension."""

    @bot.listen("on_ready")
    async def when_ready():
        """Conduct preparations once the bot is ready to go."""

        name = f"Type {bot.config.get('prefix', f'@{bot.user.name}')} help for help!"
        game = discord.Game(name=name)

        await bot.change_presence(status=discord.Status.online, game=game)
