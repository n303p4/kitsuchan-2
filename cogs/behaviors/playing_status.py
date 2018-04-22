#!/usr/bin/env python3

"""This extension sets the bot's playing status."""

import asyncio
import discord


class PlayingStatus:
    """Bot playing status manager."""

    def __init__(self, bot):
        self.bot = bot
        self.active = True
        self.statuses = []
        self.index = 0
        self.bot.loop.create_task(self.update_playing_status())

    def __unload(self):
        """If unloaded, stop pruning guilds automatically."""
        self.active = False

    def get_next_status(self):
        """Get next playing status type."""
        status = self.statuses[self.index]
        if isinstance(status, tuple):
            status = status[0].format(status[1]())
        self.index += 1
        if self.index >= len(self.statuses):
            self.index = 0
        return status

    def guild_count(self):
        """Get guild count from bot."""
        num_guilds = len(self.bot.guilds)
        return num_guilds

    def human_user_count(self):
        """Get human user cont from bot."""
        num_human_users = sum(not m.bot for m in self.bot.get_all_members())
        return num_human_users

    async def update_playing_status(self):
        """Every 10 seconds, update the bot's playing status."""
        await self.bot.wait_until_ready()

        display_prefix = self.bot.config.get('prefix', f'@{self.bot.user.name}')
        if len(display_prefix) > 1:  # No space used for single-character prefixes.
            display_prefix += " "

        self.statuses = [
            f"Type {display_prefix}help for help!",
            f"Type {display_prefix}info for info!",
            ("in {0} servers~", self.guild_count),
            ("with {0} fluffy friends~", self.human_user_count),
        ]

        while self.active:
            status = self.get_next_status()
            game = discord.Game(name=status)
            await self.bot.change_presence(status=discord.Status.online, activity=game)
            await asyncio.sleep(10)
        await self.bot.change_presence(status=discord.Status.online, activity=None)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(PlayingStatus(bot))
