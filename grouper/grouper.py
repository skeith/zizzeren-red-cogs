import discord
from discord.ext import commands
import os
from random import shuffle
from __main__ import send_cmd_help

class Grouper:
    """Groups registered people into groups"""

    def __init__(self, bot):
        self.bot = bot
        self.registered_users = []

    @commands.group(name="raid", pass_context=True)
    async def _raid(self, ctx):
        """Manage raid groups"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @_raid.command(name="register", pass_context=True)
    async def _register(self, ctx):
        """Register yourself for the next raid.
        
        You can deregister by repeating this command."""
        if ctx.message.author.id not in self.registered_users:
            self.registered_users.append(ctx.message.author.id)
            await self.bot.say("You'll be invited to the next raid!")
        else:
            self.registered_users.remove(ctx.message.author.id)
            await self.bot.say("You won't be invited to the next raid.")

    @_raid.command(name="start", pass_context=True)
    async def _start(self, ctx, size : int):
        """Groups the registered users into groups
        of size <size>."""
        shuffle(self.registered_users)
        chunks = [self.registered_users[x:x+size] for x in range(0, len(self.registered_users), size)]
        
        groups_strs = []
        for groups in chunks:
            group = []
            for user in groups:
                user = await self.bot.get_user_info(user)
                group.append(user.mention)
            groups_strs.append(", ".join(group))

        await self.bot.say("""A raid has been requested! The groups are as follows:
{}
Good luck!""".format("\n".join(groups_strs)))
        self.registered_users = []

def setup(bot):
    n = Grouper(bot)
    bot.add_cog(n)
