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
        korea = utc + timedelta(hours=9)
        
        data = "Korea :flag_kr: : {}\n".format(korea)
        data += "Singapore/Malaysia :flag_sg: : {} - (0verride's time!)\n".format(singapore)
        data += "PST :flag_us: : {}\n".format(pst)
        data += "EST :flag_ca: : {}\n".format(est)
        data += "Germany/Italy :flag_de: : {}\n".format(germany)
        data += "New Zealand :flag_nz: : {} - (Kur0's time!)\n".format(nz)
        data += "UTC :flag_gb: : {}\n".format(utc)
        await.self.bot.say(data)
        
def setup(bot):
    now = Now(bot)
    bot.add_cog(now)
