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
        shuffle(items)
        ab = [items[0], items[1]]
        cd = [items[2], items[3]]
        shuffle(ab)
        shuffle(cd)

        await self.bot.say("""PPAP~

I have a {A}, I have a {B}
Ugh~
{AB} ~

I have a {C}, I have a {D}
Ughhhh\~
{CD}\~\~\~

{AB} , {CD}...
UGHSNCSIUHNDFUISHIHDNJXNAIUHBNIJK~
{AB}-{CD}


LALALALLALALLLALALALAALLALA...
{AB}-{CD} :3""".format(A=items[0], B=items[1], C=items[2], D=items[3], AB="-".join(ab), CD="-".join(cd)))

def setup(bot):
    ppap = PPAP(bot)
    bot.add_cog(ppap)
