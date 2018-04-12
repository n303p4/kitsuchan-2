#!/usr/bin/env python3

"""Extension loading commands."""

from discord.ext import commands


class Extensions:
    """Extension loading/unloading commands."""

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension_name: str):
        """Enable the use of an extension.

        Only the bot owner can use this.
        """
        ctx.bot.config.setdefault("module_blacklist", [])
        if extension_name in ctx.bot.config["module_blacklist"]:
            ctx.bot.config["module_blacklist"].remove(extension_name)
            ctx.bot.save_config()
            try:
                ctx.bot.load_extension(extension_name)
                await ctx.send(f"Loaded extension {extension_name}")
                return
            except Exception as error:
                await ctx.send(error)
                return
        await ctx.send(f"{extension_name} is already loaded.")

    @commands.group(aliases=["reload", "rloade"], invoke_without_command=True)
    @commands.is_owner()
    async def rload(self, ctx, extension_name: str):
        """Reload an already-loaded extension.

        Only the bot owner can use this.
        """
        ctx.bot.unload_extension(extension_name)
        ctx.bot.load_extension(extension_name)
        await ctx.send(f"{extension_name} reloaded.")

    @rload.command(name="--all", aliases=["-a"])
    @commands.is_owner()
    async def reloadall(self, ctx):
        """Reload all modules."""
        for extension in list(ctx.bot.extensions):
            try:
                ctx.bot.unload_extension(extension)
                ctx.bot.load_extension(extension)
            except Exception as e:
                await ctx.send((f"Could not reload extension {extension}: "
                                f"{e}"))

        await ctx.send(f"Reloaded all modules.")

    @commands.command(aliases=["unload", "uloade"])
    @commands.is_owner()
    async def uload(self, ctx, extension_name: str):
        """Disable the use of an extension.

        Only the bot owner can use this."""
        ctx.bot.config.setdefault("module_blacklist", [])
        if extension_name not in ctx.bot.config["module_blacklist"]:
            ctx.bot.config["module_blacklist"].append(extension_name)
            ctx.bot.save_config()
            try:
                ctx.bot.unload_extension(extension_name)
                await ctx.send(f"Unloaded extension {extension_name}")
                return
            except Exception as error:
                await ctx.send(error)
                return
        await ctx.send(f"{extension_name} is not currently loaded.")


def setup(bot):
    """Sets up the cog."""
    bot.add_cog(Extensions())
