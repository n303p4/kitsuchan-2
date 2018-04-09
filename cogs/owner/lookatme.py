#!/usr/bin/env python3

"""Extension that contains a bots.discord.pw server count updater."""

BASE_URL_DBOTS_API = "https://bots.discord.pw/api/bots/{0}/stats"


async def lookatme(ctx):
    """Update the bot's server count on bots.discord.pw."""
    token = ctx.bot.config.get("dbots_token", None)

    if not token:
        await ctx.send("No token specified in the config.")
        return

    url = BASE_URL_DBOTS_API.format(ctx.bot.user.id)

    data = {"server_count": len(ctx.bot.guilds), "shard_id": ctx.bot.shard_id,
            "shard_count": ctx.bot.shard_count}
    headers = {"Authorization": token}

    async with ctx.bot.session.request("POST", url, json=data, headers=headers):
        pass


def setup(bot):
    """Set up the extension."""

    @bot.listen("on_guild_join")
    async def handle_guild_join(ctx):
        """Trigger lookatme on guild join."""
        await lookatme(ctx)

    @bot.listen("on_guild_remove")
    async def handle_guild_remove(ctx):
        """Trigger lookatme on guild leave."""
        await lookatme(ctx)
