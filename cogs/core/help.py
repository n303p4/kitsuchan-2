#!/usr/bin/env python3

import discord
from discord.ext import commands


class Help:
    """Help command."""

    @commands.command(aliases=["commands"])
    @commands.cooldown(1, 2)
    async def help(self, ctx, *cmds: str):
        """Help command.

        * command_or_cog - The name of a command or cog.
        """
        if not cmds:
            embed = discord.Embed(title="List of commands")
            commands_list = {}
            for command in ctx.bot.commands:
                if command.hidden:
                    continue
                try:
                    can_run = await command.can_run(ctx)
                except Exception:
                    continue
                if can_run:
                    if command.cog_name:
                        commands_list.setdefault(command.cog_name, []).append(command.name)
            for key in sorted(list(commands_list.keys())):  # TODO Not scalable past 25 cogs
                embed.add_field(name=key, value=", ".join(sorted(commands_list[key])))
            embed.set_footer(text=(f"Run \"{ctx.invoked_with} command\" for "
                                   "more details on a command."))
            await ctx.send(embed=embed)
        else:
            # This is awful, haha
            await ctx.bot.all_commands["old_help"].callback(ctx, *cmds)


def setup(bot):
    """Set up the extension."""
    try:
        help_command = bot.all_commands["help"]
        help_command.hidden = True
        help_command.name = "old_help"
        bot.remove_command("help")
        bot.add_command(help_command)
    except KeyError:  # This means the setup already did its thing.
        pass
    bot.add_cog(Help())
