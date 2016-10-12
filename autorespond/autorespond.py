import discord
from discord.ext import commands
from .utils.dataIO import fileIO
from .utils import checks
from random import choice
from __main__ import send_cmd_help
from __main__ import *
from time import sleep

class AutoRespond:

    def __init__(self, bot):
        self.bot = bot
        self.responses = fileIO("data/autorespond/responses.json", "load")
        self.settings = fileIO("data/autorespond/settings.json", "load")

    async def recvMessage(self, message):
        msg = message.content
        sentMessage = None
        if (message.author.id != self.bot.user.id):
            for key, response in self.responses.items():
                if key in msg.lower():
                    sentMessage = await self.bot.send_message(message.channel, choice(response))
        
        if sentMessage == None or self.settings["deleteTime"] == 0:
            return
        # Wait a number of seconds
        sleep(self.settings["deleteTime"])
        # Delete the message
        await self.bot.delete_message(sentMessage)


    @commands.group(name="responses", pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def _responses(self, ctx):
        """Manage automatic responses"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @_responses.command(name="add")
    async def _add(self, *ctx : str):
        """Adds an automatic response to Red's set

        Accepts two strings, enclosed in double quotes: The trigger, and the response.
        Example:
        +responses add \"ping\" \"pong\" """

        if ctx == () or "" in ctx or len(ctx) < 2:
            await self.bot.say("I need at least two strings.")
            return

        trigger, *responses = ctx
        trigger = trigger.lower()
        if trigger in self.responses:
            currentResponses = set(self.responses[trigger])
            self.responses[trigger] = list(set(responses) | currentResponses)
        else: self.responses[trigger] = list(responses)
        fileIO("data/autorespond/responses.json", "save", self.responses)

        items = "\"" + trigger + "\"" + " : " + ', '.join('"{0}"'.format(w) for w in responses)
        await self.bot.say("Added `" + items + "` to automatic responses")

    @_responses.command(name="remove")
    async def _remove(self, *ctx : str):
        """Removes an automatic response from Red's set

        Accepts two strings, enclosed in double quotes: The trigger, and the response.
        Example:
        +responses add \"ping\" \"pong\" """

        if ctx == () or "" in ctx or len(ctx) < 1:
            await self.bot.say("I need at least one string.")
            return

        if len(ctx) == 1:
            del(self.responses[ctx[0]])
            await self.bot.say("Removed `" + ctx[0] + "` from automatic responses.")
            return

        trigger, *responses = ctx
        trigger = trigger.lower()
        currentResponses = set(self.responses[trigger])
        self.responses[trigger] = list(currentResponses - set(responses))

        if not self.responses[trigger]:
            del(self.responses[trigger])

        fileIO("data/autorespond/responses.json", "save", self.responses)

        items = "\"" + trigger + "\"" + " : " + ', '.join('"{0}"'.format(w) for w in responses)
        await self.bot.say("Removed `" + items + "` from automatic responses.")

    @_responses.command(name="list")
    async def _list(self):
        """Lists the current autoReponse list."""

        items = ""
        for key, response in self.responses.items():
            items += key + " : " + ', '.join('"{0}"'.format(w) for w in response) + "\n"
        if self.settings["deleteTime"] == 0:
            deleteString = "Automatic responses will not be deleted."
        else:
            deleteString = "Automatic responses will be deleted after {} seconds.".format(self.settings["deleteTime"])
        await self.bot.say("Current automatic responses: \n```{}```{}".format(items, deleteString))

    @_responses.command(name="timeout")
    async def _timeout(self, ctx):
        """Sets the timeout to delete a sent automatic response.
        
        Accepts an integer, in seconds. If set to zero, messages are never deleted."""
        self.settings["deleteTime"] = int(ctx)
        fileIO("data/autorespond/settings.json", "save", self.settings)
        if ctx == 0:
            await self.bot.say("Automatic responses will not be deleted.")
        else:
            await self.bot.say("Automatic responses will be deleted after {} seconds.".format(ctx))

def check_folders():
    if not os.path.exists("data/autorespond"):
        print("Creating data/autorespond folder...")
        os.makedirs("data/autorespond")

def check_files():
    defaultResponses = { "skynet" : [ "Hi! :wave:" ] }
    defaultSettings = { "deleteTime" : 0 }

    f = "data/autorespond/responses.json"
    if not fileIO(f, "check"):
        print("Creating empty responses.json..")
        fileIO(f, "save", defaultResponses)
    f = "data/autorespond/settings.json"
    if not fileIO(f, "check"):
        print ("Creating empty autorespond settings...")
        fileIO(f, "save", defaultSettings)

def setup(bot):
    check_folders()
    check_files()
    n = AutoRespond(bot)
    bot.add_listener(n.recvMessage, "on_message")
    bot.add_cog(n)
