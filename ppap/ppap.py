import discord
from discord.ext import commands
from random import shuffle

class PPAP:
    """PEN PINEAPPLE APPLE PEN"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ppap(self, ctx, a, b, c, d):
        """PPAP"""
        items = [a, b, c, d]
        ab = [a, b]
        cd = [c, d]
        shuffle(items)
        shuffle(ab)
        shuffle(cd)

        await self.bot.say("""PPAP~

I have a {A}, I have a {B}
Ugh~
{AB} ~

I have a {C}, I have a {D}
Ughhhh\~
{CD}\~\~\~

{A}-{B} , {C}-{D}...
UGHSNCSIUHNDFUISHIHDNJXNAIUHBNIJK~
{A}-{B}-{C}-{D}


LALALALLALALLLALALALAALLALA...
{A}{B}{C}{D} :3""".format(A=items[0], B=items[1], C=items[2], D=items[3], AB=ab, CD=cd))

def setup(bot):
    ppap = PPAP(bot)
    bot.add_cog(ppap)
