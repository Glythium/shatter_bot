import os
from twitchio.ext import commands

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            irc_token=os.environ['TMI_TOKEN'],
            client_id=os.environ['CLIENT_ID'],
            nick=os.environ['BOT_NICK'],
            prefix=os.environ['BOT_PREFIX'],
            initial_channels=[os.environ['CHANNEL']]
        )

    async def event_ready(self):
        'Called once when the bot goes online.'
        print(f"{os.environ['BOT_NICK']} is in {os.environ['CHANNEL']}'s chat!")


    async def event_message(self, ctx):
        'Runs every time a message is sent in chat.'

        # make sure the bot ignores itself and the streamer
        if ctx.author.name.lower() == os.environ['BOT_NICK'].lower():
            return
        
        await bot.handle_commands(ctx)

        if 'hello' in ctx.content.lower():
            await ctx.channel.send(f"Hi, @{ctx.author.name}!")
        

############################## Commands #######################################
    @commands.command(name='help')
    async def help(self, ctx):
        # Usage statement???
        await ctx.send(f"There's no help for you, @{ctx.author.name}")

    @commands.command(name='clip')
    async def clip(self, ctx):
        # Make a clip
        await ctx.send(f"Coming Soon!")

    @commands.command(name='roll')
    async def roll(self, ctx):
        # Some kind of RNG
        await ctx.send(f"Coming Soon!")
    
    @commands.command(name="goodBot")
    async def goodBot(self, ctx):
        # Bots need lovin'
        await ctx.send(f"Coming Soon!")
    
    @commands.command(name="badBot")
    async def badBot(self, ctx):
        # Bots need hatin'
        await ctx.send(f"Coming Soon!")


if __name__ == "__main__":
    bot = Bot()
    bot.run()