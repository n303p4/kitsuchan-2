#!/usr/bin/env python3

import logging

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

FILENAME_BLACKLIST = "blacklist.json"


class Blacklisting:
    """Blacklisting commands, to prevent abusive usage of the bot.

    These won't show up unless you're the bot owner.
    """

    def __init__(self, bot):
        self.bot = bot
        # self.bot.loop.add_task(self.prune_guilds_auto)
        self.settings = {}
        self.load()
        self.bot.check(self.blacklist_user)
        self.bot.check(self.blacklist_guild)

        @bot.listen("on_guild_join")
        async def check_guild(guild):
            await self.prune_guild(guild)

    async def prune_guild(self, guild: discord.Guild):
        """Automatically prune a guild."""
        num_humans = sum(not member.bot for member in guild.members)
        num_bots = sum(member.bot for member in guild.members)
        collection = (num_bots/(num_bots + num_humans) >= 0.6) and num_bots > 50
        logger.debug(f"Checking guild {guild.name} ({guild.id}) (collection: {collection})...")
        if collection:
            await guild.leave()
            return "bot collection"
        elif guild.id in self.settings.get("guilds"):
            await guild.leave()
            return "guild blacklisted"
        elif guild.owner.id in self.settings.get("users"):
            await guild.leave()
            return "user blacklisted"

    @commands.command()
    @commands.is_owner()
    async def prune_guilds(self, ctx):
        """Automatically leave guilds."""
        number = 0
        paginator = commands.Paginator()
        for guild in self.bot.guilds:
            reason = await self.prune_guild(guild)
            if reason:
                message = (f"Automatically left guild {guild.name} ({guild.id}) "
                           f"(reason: {reason})")
                logger.info(message)
                paginator.add_line(message)
                number += 1
        for page in paginator.pages:
            await ctx.send(page)
        if number > 0:
            message = f"{number} guilds were pruned."
            logger.info(message)
            await ctx.send(message)
        else:
            await ctx.send("No guilds pruned.")
        return number

    def load(self):
        try:
            self.settings = self.bot.config["blacklist"]
        except Exception:
            self.save()

    def save(self):
        self.settings.setdefault("users", [])
        self.settings.setdefault("guilds", [])
        self.bot.config["blacklist"] = self.settings
        self.bot.save_config()

    def blacklist_user(self, ctx):
        return ctx.author.id not in self.settings.get("users")

    def blacklist_guild(self, ctx):
        if ctx.guild:
            return ctx.guild.id not in self.settings.get("guilds")
        return True

    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def block(self, ctx):
        """Blocking commands (e.g. block user). Bot owner only."""
        pass

    @block.command(name="user")
    @commands.is_owner()
    async def _blockuser(self, ctx, user_id: int):
        """Block a user. Only the bot owner can use this.

        * user_id - The ID of the user to block.
        """
        self.settings.setdefault("users", [])
        app_info = await ctx.bot.application_info()
        is_owner = user_id == app_info.owner.id
        if is_owner:
            message = "Can't block bot owner."
            logger.warning(message)
            raise commands.UserInputError(message)
        if user_id not in self.settings["users"]:
            self.settings["users"].append(user_id)
            message = f"{user_id} blocked."
            logger.info(message)
            await ctx.send(message)
            await self.prune_guilds()
        else:
            message = f"{user_id} already blocked."
            logger.info(message)
            await ctx.send(message)
        self.save()

    @block.command(name="guild", aliases=["server"])
    @commands.is_owner()
    async def _blockguild(self, ctx, guild_id: int):
        """Block a guild. Only the bot owner can use this.

        * guild_id - The ID of the guild to block.
        """
        self.settings.setdefault("guilds", [])
        if guild_id not in self.settings["guilds"]:
            self.settings["guilds"].append(guild_id)
            message = f"{guild_id} blocked."
            logger.info(message)
            await ctx.send(message)
            try:
                guild = ctx.bot.get_guild(guild_id)
                await self.prune_guild(guild)
                await guild.leave()
            except Exception:
                pass
        else:
            message = f"{guild.name} already blocked."
            logger.info(message)
            await ctx.send(message)
        self.save()

    @commands.group(aliases=["ublock"], invoke_without_command=True)
    @commands.is_owner()
    async def unblock(self, ctx):
        """Unblocking commands (e.g. unblock user). Bot owner only."""
        pass

    @unblock.command(name="user")
    @commands.is_owner()
    async def _unblockuser(self, ctx, user_id: int):
        """Unblock a user. Only the bot owner can use this.

        * user_id - The user ID to unblock.
        """
        self.settings.setdefault("users", [])
        if user_id in self.settings["users"]:
            self.settings["users"].remove(user_id)
            message = f"{user_id} unblocked."
            logger.info(message)
            await ctx.send(message)
        else:
            await ctx.send(f"{user_id} already unblocked.")
        self.save()

    @unblock.command(name="guild", aliases=["server"])
    @commands.is_owner()
    async def _unblockguild(self, ctx, guild_id: int):
        """Unblock a guild. Only the bot owner can use this.

        * guild_id - The ID of the guild to unblock.
        """
        self.settings.setdefault("guilds", [])
        if guild_id in self.settings["guilds"]:
            self.settings["guilds"].remove(guild_id)
            message = f"{guild_id} unblocked."
            logger.info(message)
            await ctx.send(message)
        else:
            message = f"{guild_id} already unblocked."
            logger.info(message)
            await ctx.send(message)
        self.save()


def setup(bot):
    bot.add_cog(Blacklisting(bot))
