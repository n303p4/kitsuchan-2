#!/usr/bin/env python3

import asyncio
import logging

logger = logging.getLogger(__name__)


class BotCollectionKiller:
    """Bot collection pruning."""

    def __init__(self, bot):
        self.bot = bot

        @bot.listen("on_guild_join")
        async def check_guild(guild):
            """Check to prune a guild on join."""
            await self.prune_guild(guild)

        self.active = True
        self.bot.loop.create_task(self.prune_guilds_auto())

    def __unload(self):
        """If unloaded, stop pruning guilds automatically."""
        self.active = False

    async def prune_guild(self, guild):
        """Check a guild to see if it's a bot collection, and leave it if it is."""
        num_humans = sum(not member.bot for member in guild.members)
        num_bots = sum(member.bot for member in guild.members)
        collection = (num_bots/(num_bots + num_humans) >= 0.6) and num_bots > 50
        logger.debug(f"Checking guild {guild.name} ({guild.id}) (collection: {collection})...")
        if collection:
            await guild.leave()
            return "bot collection"

    async def prune_guilds(self):
        """Iterate over all guilds and leave those that are computed to be bot collections."""
        number = 0

        for guild in self.bot.guilds:
            reason = await self.prune_guild(guild)
            if reason:
                message = (f"Automatically left guild {guild.name} ({guild.id}) "
                           f"(reason: {reason})")
                logger.info(message)
                number += 1

        if number > 0:
            message = f"{number} guilds were pruned."
            logger.info(message)
        else:
            logger.info("No guilds pruned.")

        return number

    async def prune_guilds_auto(self):
        """Iterate over all guilds every thirty seconds and leave any bot collections."""
        await self.bot.wait_until_ready()
        while self.active:
            await self.prune_guilds()
            await asyncio.sleep(30)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(BotCollectionKiller(bot))
