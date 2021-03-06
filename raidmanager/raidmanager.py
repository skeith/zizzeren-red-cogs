import discord
from discord.ext import commands
import os
from random import shuffle
from __main__ import send_cmd_help
import time

def seconds_to_string(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h == 0:
        return "{} minutes".format(int(m))
    else:
        return "{} hours".format(int(h))

class RaidManager:
    """Groups registered people into groups"""

    def __init__(self, bot):
        self.bot = bot
        # Looks like 
        # { "user.id" : { "mention" : discord.Mention, "type" : "pq", "start_time" : 123456, "length" : 1234 } }
        self.registered_users = {}
        self.raid_types = ["pq", "raidersraid", "countraids", "everything"]
        self.units = {"minute" : 60, "minutes" : 60, "hour" : 3600, "hours" : 3600}

    def check_expired(self):
        to_remove = []
        for user, data in self.registered_users.items():
            if data["start_time"] + data["length"] <= int(time.time()):
                to_remove.append(user)
        for user in to_remove:
            del self.registered_users[user]

    @commands.group(name="raid", pass_context=True)
    async def _raid(self, ctx):
        """Manage raid groups"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @_raid.command(name="register", pass_context=True)
    async def _register(self, ctx, raid_type : str, start_time : int, u_start_time : str, length : int, u_length : str):
        """Register yourself for the next raid. 
        Usage:
        [p]raid register <raid-type> <start-time units> <length units>

        where raid-type is: 
        "PQ", "RaidersRaid", "CountRaids", or "Everything"
        <start_time u_start_time> and <length u_length> are like '4 hours'"""
        # Sanity checking
        if raid_type.lower() not in self.raid_types:
            await self.bot.say("That's not a valid raid type! Try `{}`".format(", ".join(self.raid_types)))
            return
        if u_start_time.lower() not in self.units or u_length.lower() not in self.units:
            await self.bot.say("That's not a time unit! Try `{}`".format(", ".join(self.units)))
            return

        start_time_seconds = self.units[u_start_time] * start_time
        start_time_future = int(time.time() + start_time_seconds)
        length_seconds = self.units[u_length] * length

        self.registered_users[ctx.message.author] = { "mention" : ctx.message.author.mention, "type" : raid_type.lower(), "start_time" : start_time_future, "length" : length_seconds }

        await self.bot.say("You've been registered for raid type: {}, starting {} {} from now, and you're free for {} {}!".format(raid_type, start_time, u_start_time, length, u_length))

    @_raid.command(name="start", pass_context=True)
    async def _start(self, ctx, raid_type : str, size : int, time_away : int, t_units : str):
        """Start a raid!

        Specify your group size, what kind of raid you want, and when you want to start:
        [p]raid start <type> <size> <time_away units>
        where <type> is "PQ", "RaidersRaid", "CountRaids", "Everything"
        and <time_away units> is like '10 minutes'.
        Valid units are minutes and hours."""

        self.check_expired()

        # Sanity checking
        if raid_type.lower() not in self.raid_types:
            await self.bot.say("That's not a valid raid type! Try `{}`".format(", ".join(self.raid_types)))
            return
        if t_units.lower() not in self.units:
            await self.bot.say("That's not a time unit! Try `{}`".format(", ".join(self.units)))
            return

        # { "user.id" : { "mention" : discord.Mention, "type" : "pq", "start_time" : 123456, "length" : 1234 } }
        start_time_seconds = self.units[t_units] * time_away
        start_time_future = int(time.time() + start_time_seconds)
        # For all the users in the specified raid type
        #   If the start time lands in their available time window
        #       Add them to the raid group
        group = []
        
        for user, data in self.registered_users.items():
            if data["type"].lower() == raid_type.lower():
                if start_time_future <= data["start_time"] + data["length"]:
                    if start_time_future >= data["start_time"]:
                        group.append(user)

        # Randomise the raid group, and chunk it into several groups of the specified size
        
        shuffle(group)
        chunks = [group[x:x+size] for x in range(0, len(group), size)]

        groups_strs = []
        for groups in chunks:
            group = []
            for user in groups:
                user = self.registered_users[user]["mention"]
                group.append(user)
            groups_strs.append(", ".join(group))

        await self.bot.say("""A **{}** raid has been requested! The groups are as follows:
        {}\nGood luck!""".format(raid_type, "\n        ".join(groups_strs)))


    @_raid.command(name="list", pass_context=True)
    async def _list(self, ctx):
        """Shows who is registered for what raid, and when."""
        self.check_expired()

        # For each element in self.registered_users
        # Add them to users_by_type as an element of the array indexed by key "type"
        # This has data { "mention" : discord.Mention", "start_time" : int, "length" : int }
        users_by_type = {"pq" : [], "raidersraid" : [], "countraids" : [], "everything" : []}
        for user, data in self.registered_users.items():
            if data["start_time"] - int(time.time()) <= 0:
                # Their period has begun
                users_by_type[data["type"]].append("{}: Ready now, and for another {}!".format(data["mention"], seconds_to_string(data["length"] - (time.time() - data["start_time"]))))
            else:
                # Their period is in the future
                users_by_type[data["type"]].append("{}: {} from now, for {}".format(data["mention"], seconds_to_string(data["start_time"] - int(time.time())), seconds_to_string(data["length"])))

        # For each element in users_by_type
        # Format a string for each user describing the contents of their data
        type_strs = []
        for raid_type, data in users_by_type.items():
            type_strs.append("**{}:**\n{}".format(raid_type, "\n".join(data)))

        await self.bot.say("Registered users for upcoming raids:\n{}".format("\n".join(type_strs)))

    @_raid.command(name="clear", pass_context=True)
    async def _clear(self, ctx):
        """Clear yourself from any upcoming raids."""
        del self.registered_users[ctx.message.author]
        await self.bot.say("You've been cleared from the upcoming raids.")

def setup(bot):
    n = RaidManager(bot)
    bot.add_cog(n)
