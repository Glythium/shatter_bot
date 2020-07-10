import os
import random
import time
from twitchio.ext import commands


class CoolDownManager():
    def __init__(self, timer):
        self.timer = timer
        self.start = time.time()
        self.multiplier = {
            "sec": 1,
            "second": 1,
            "seconds": 1,
            "min": 60,
            "minute": 60,
            "minutes": 60,
            "hour": 3600,
            "hours": 3600
        }

    def updateCooldown(self, number, unit):
        try:
            new_time = number * self.multiplier[unit]
        except KeyError:
            return None
        self.timer = new_time
        return "{} {}".format(str(number), unit)
    
    def isCool(self):
        if time.time() - self.start >= self.timer:
            self.start = time.time()
            return True
        return False


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            irc_token=os.environ['TMI_TOKEN'],
            client_id=os.environ['CLIENT_ID'],
            nick=os.environ['BOT_NICK'],
            prefix=os.environ['BOT_PREFIX'],
            initial_channels=[os.environ['CHANNEL']]
        )
        self.cooldownMgr = CoolDownManager(5)

######################### Personality #########################################
        self.catchPhrases = [
            "Part-time bot, full-time edgelord.",
            "Don't hurt yourself, kid.",
            "It's time to shatter and splatter.",
            "One more for the road."
        ]
        self.quips = [
            "So...you have chosen death", 
            "I may not have eyes, but I know what a scrub looks like",
            "4/5 dentists recommend you stop trying so hard",
            "I'm cookin' up knuckle sandwiches with extra beef"
        ]
        self.thanks = [
            "Thank you kindly",
            "I aim to please",
            "You're alright",
            "All in a day's work",
            "uwu"
        ]
        self.jeers = [
            "You just made the list",
            "Bots have feelings too",
            "Oh, come on",
            "I'll ignore that one",
        ]
        self.iceBreakers = [
            "What's your favorite videogame",
        ]
        self.goodWords = [
            "like",
            "love",
            "good",
            "great",
            "awesome",
            "best",
            "right",
            "cheer",
            "chat"
        ]
        self.badWords = [
            "bad",
            "worse",
            "terrible",
            "horrible",
            "awful",
            "hate",
            "suck",
            "stink",
            "problem"
        ]

################################ Actual Functions #############################
    def randShoutout(self, username):
        'Randomly tacks on the @username'
        name = random.choice(["", '@' + username])
        return name

    async def event_ready(self):
        'Called once when the bot goes online.'
        print(f"{os.environ['BOT_NICK']} is in {os.environ['CHANNEL']}'s chat!")

    async def event_message(self, ctx):
        'Runs every time a message is sent in chat.'
        # make sure the bot ignores itself
        if ctx.author.name.lower() == os.environ['BOT_NICK'].lower():
            return
        
        await bot.handle_commands(ctx)

        if self.cooldownMgr.isCool():
            if any(word in ctx.content.lower() for word in self.goodWords):
                await ctx.channel.send(f"{random.choice(self.catchPhrases)}")
            elif any(word in ctx.content.lower() for word in self.badWords):
                await ctx.channel.send(f"{random.choice(self.quips)} {self.randShoutout(ctx.author.name)}")

        if 'hello' in ctx.content.lower():
            await ctx.channel.send(f"Hi, @{ctx.author.name}!")
        elif 'bye' in ctx.content.lower():
            await ctx.shannel.send(f"Bye, @{ctx.author.name}")


############################## Commands #######################################
    @commands.command(name='help')
    async def help(self, ctx):
        # Usage statement???
        await ctx.send(f"I can't help you, @{ctx.author.name}")

    @commands.command(name='roll')
    async def roll(self, ctx):
        try:
            args = ctx.content.lower().split()
            number = int(args[1])
            await ctx.send(f"@{ctx.author.name} rolled a {random.randint(1,number)}!")
        except:
            await ctx.send(f"Usage: !roll <number>")
    
    @commands.command(name="goodBot")
    async def goodBot(self, ctx):
        # Bots need lovin'
        await ctx.send(f"{random.choice(self.thanks)} {self.randShoutout(ctx.author.name)}")
    
    @commands.command(name="badBot")
    async def badBot(self, ctx):
        # Bots need hatin'
        await ctx.send(f"{random.choice(self.jeers)} {self.randShoutout(ctx.author.name)}")
    
    @commands.command(name='cooldown')
    async def setCooldown(self, ctx):
        # Set a new cooldown timer
        if ctx.author.is_mod:
            args = ctx.content.lower().split()
            number = int(args[1])
            unit = args[2].lower()
            new_time = self.cooldownMgr.updateCooldown(number, unit)
            if new_time is None:
                await ctx.send(f"Usage !cooldown <number> <sec/min/hour>")
            else:
                await ctx.send(f"Set cooldown for {new_time}!")


if __name__ == "__main__":
    random.seed()
    bot = Bot()
    bot.run()