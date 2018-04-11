#!/usr/bin/env python3

import datetime

from curious.commands.context import Context
from curious.commands.decorators import command, ratelimit
from curious.commands.plugin import Plugin
from curious.commands.ratelimit import BucketNamer


class Ping(Plugin):
    """Ping command."""

    @command()
    @ratelimit(limit=6, time=12, bucket_namer=BucketNamer.GLOBAL)
    async def ping(self, ctx: Context):
        """Ping the bot."""
        pingtime = int(round((datetime.datetime.utcnow() -
                              ctx.message.created_at).total_seconds() * 1000, 0))
        message = f":ping_pong: {pingtime} ms!"
        await ctx.channel.messages.send(message)
