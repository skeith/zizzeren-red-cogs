import discord
from discord.ext import commands
from .utils.dataIO import fileIO
import os
import time
from datetime import datetime, timedelta
import logging

class Now:
    """Whee, timezones!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def now(self, ctx):
        """Says the time in a bunch of timezones."""
        utc = datetime.utcnow()
        nz = utc + timedelta(hours=13)
        singapore = utc + timedelta(hours=8)
        pst = utc + timedelta(hours=-7)
        est = utc + timedelta(hours=-3)
        germany = utc + timedelta(hours=2)
        korea = utc + timedela(hours=9)

        await self.bot.say("""
Korea                            - {}    :flag_kr:
Singapore/Malaysia  - {}    :flag_sg: (0verride's time!)
PST                                - {}    :flag_us:
EST                                - {}    :flag_ca:
Germany/Italy            - {}    :flag_de:
New Zealand               - {}    :flag_nz: (Kur0's time!)
UTC                               - {}    :flag_gb:""".format(singapore, pst, est, germany, nz, utc))

def setup(bot):
    now = Now(bot)
    bot.add_cog(now)
