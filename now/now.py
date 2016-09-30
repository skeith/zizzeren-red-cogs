import discord
from discord.ext import commands
from .utils.dataIO import fileIO
import os
import time
import datetime
import logging

class Now:
    """Whee, timezones!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def now(self, ctx):
        """Says the time in a bunch of timezones."""
        utc = datetime.datetime.utcnow()
        nz = utc + timedelta(hours=12)
        singapore = utc + timedelta(hours=8)
        pst = utc + timedelta(hours=-8)
        est = utc + timedelta(hours=-4)
        germany = utc + timedelta(hours=1)

        await self.bot.say("```
        Singapore/Malaysia  - {}    (0verride's time! :flag_sg:)
        PST                 - {}
        EST                 - {}
        Germany/Italy       - {}
        Italy               - {}
        New Zealand         - {}    (Kur0's time! :flag_nz:)
        UTC                 - {}
        ```".format(singapore, pst, est, germany, nz, utc))

def setup(bot):
    n = RemindMeRepeat(bot)
    bot.add_cog(n)
