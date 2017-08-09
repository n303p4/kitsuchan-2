#!/usr/bin/env python3

"""Contains a cog that fetches discriminators."""

from discord.ext import commands


class Discriminator:
    """Discriminator command."""

    @commands.command(aliases=["discriminator"])
    @commands.guild_only()
    @commands.cooldown(6, 12)
    async def discrim(self, ctx, *, discriminator: str=None):
        """Find all users the bot can see with a given discriminator.

        * discriminator - (optional) A discriminator to search for."""

        if not discriminator:
            discriminator = str(ctx.author.discriminator)
        discriminator = discriminator.replace("#", "")  # Eliminate pound signs.

        results = []
        for user in ctx.bot.users:
            if str(user.discriminator) == discriminator.zfill(4):
                results.append(f"{len(results)+1}. {user.name}#{user.discriminator}")

        if not results:
            await ctx.send(f"Couldn't find anyone with that discriminator. :<")

        else:
            paginator = commands.Paginator(prefix="```markdown")
            paginator.add_line(f"* Guilds searched: {len(ctx.bot.guilds)}")
            paginator.add_line(f"* Users found: {len(results)}")
            paginator.add_line("")

            for member in results[:10]:
                paginator.add_line(member)

            if len(results) > 10:
                paginator.add_line(f"...and {len(results)-10} others.")

            await ctx.send(paginator.pages[0])


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Discriminator())
