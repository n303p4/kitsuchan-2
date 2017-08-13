#!/usr/bin/env python3

"""Extension that contains a bots.discord.pw server count updater."""

from discord.ext import commands

BASE_URL_DBOTS_API = "https://bots.discord.pw/api/bots/{0}/stats"


class LookAtMe:
    """Contains a command which updates the bot's server count on Discord Bots."""

    @commands.command()
    @commands.is_owner()
    async def lookatme(self, ctx):
        """Update the bot's server count on bots.discord.pw. Bot owner only."""
        token = ctx.bot.config.get("dbots_token", None)
        
        if not token:
            await ctx.send("No token specified in the config.")

        url = BASE_URL_DBOTS_API.format(ctx.bot.user.id)
        
        data = {"server_count": len(ctx.bot.guilds), "shard_id": ctx.bot.shard_id,
                "shard_count": ctx.bot.shard_count}
        headers = {"Authorization": token}
        
        async with ctx.bot.session.request("POST", url, json=data, headers=headers) as response:
            if response.status <= 210:
                await ctx.send("POSTing OK.")
            else:
                await ctx.send("POSTing failed.")


def setup(bot):
    """Set up the extension."""
    bot.add_cog(LookAtMe(bot))
