#!/usr/bin/env python3

"""Extension that contains a bots.discord.pw server count updater."""

BASE_URL_DBOTS_API = "https://bots.discord.pw/api/bots/{0}/stats"


def setup(bot):
    """Set up the extension."""

    token = bot.config.get("dbots_token", None)

    if not token:
        return

    async def lookatme():
        """Update the bot's server count on bots.discord.pw."""

        url = BASE_URL_DBOTS_API.format(bot.user.id)

        data = {"server_count": len(bot.guilds), "shard_id": bot.shard_id,
                "shard_count": bot.shard_count}
        headers = {"Authorization": token}

        async with bot.session.request("POST", url, json=data, headers=headers):
            pass

    @bot.listen("on_guild_join")
    async def handle_guild_join(guild):
        """Trigger lookatme on guild join."""
        await lookatme()

    @bot.listen("on_guild_remove")
    async def handle_guild_remove(guild):
        """Trigger lookatme on guild leave."""
        await lookatme()
