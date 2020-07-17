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
            "min": 60,
            "hour": 3600
        }

    def updateCooldown(self, number, unit):
        try:
            if unit in ["second", "seconds"]:
                unit = "sec"
            elif unit in ["minute", "minutes"]:
                unit = "min"
            elif unit == "hours":
                unit = "hour"
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
        self.levelQueue = []
        self.canAddLevels = True

######################### Personality #########################################
        self.catchPhrases = [
            "Part-time bot, full-time edgelord.",
            "Don't hurt yourself, kid.",
            "It's time to shatter and splatter.",
            "It's time to D-D-D-DUEL!",
            "Can you smell what this bot is cookin'?",
            "Simpin' ain't easy..."
        ]
        self.quips = [
            "So...you have chosen death", 
            "I may not have eyes, but I know what a scrub looks like",
            "4/5 dentists recommend you stop failing so hard",
            "I'm cookin' up knuckle sandwiches with extra beef",
            "In these uncertain times, we can all count on you being trash",
            "Everyone here is dumber for having heard you speak",
        ]
        self.thanks = [
            "Thank you kind stranger",
            "I aim to please",
            "You're alright",
            "All in a day's work",
            "uwu",
            "Hail to the king,",
        ]
        self.jeers = [
            "You just made the list",
            "Bots have feelings too",
            "Oh, come on",
            "I'll ignore that one",
            "Bite me",
            "Oooo, yes...harder"
        ]
        self.noPerms = [
            "You're not my supervisor",
            "Whatever, I do what I want",
            "Not right now, I have a headache",
            "I can't let you do that",
            "You don't have enough badges to train me",
            "No, no, a thousand times no"
        ]
        self.iceBreakers = [
            "What's your favorite videogame",
            "Which Pokemon would you eat, if you could"
        ]
        self.goodWords = [
            "love ",
            "good ",
            "great ",
            "awesome ",
            "best ",
            "right ",
            "cheer ",
            "chat "
        ]
        self.badWords = [
            "bad ",
            "worse ",
            "worst ",
            "terrible ",
            "horrible ",
            "awful ",
            "hate ",
            "suck ",
            "stink ",
        ]

################################ Actual Functions #############################
    def randShoutout(self, username):
        'Randomly tacks on the @username, nothing, or meatbag'
        name = random.choice(["", '@' + username, "meatbag"])
        return name

    async def event_ready(self):
        'Called once when the bot goes online.'
        print(f"{os.environ['BOT_NICK']} is in {os.environ['CHANNEL']}'s chat!")

    async def event_message(self, ctx):
        'Runs every time a message is sent in chat.'
        # make sure the bot ignores itself
        if ctx.author.name.lower() == os.environ['BOT_NICK'].lower():
            return
        
        # Always handle commands as they come in.
        await bot.handle_commands(ctx)
        print(f"{ctx.content}")

        # Don't interact with chat if you're on cool down.
        if self.cooldownMgr.isCool():
            if any(word in ctx.content.lower() for word in self.goodWords):
                await ctx.channel.send(f"{random.choice(self.catchPhrases)}")
            elif any(word in ctx.content.lower() for word in self.badWords):
                await ctx.channel.send(f"{random.choice(self.quips)} {self.randShoutout(ctx.author.name)}")

        # Always say hi and bye if prompted.
        if any(word in ctx.content.lower() for word in ("hello ", "hi ", "heya ")):
            await ctx.channel.send(f"Hi, @{ctx.author.name}!")
        elif any(word in ctx.content.lower() for word in ("bye ", "goodnight ")):
            await ctx.channel.send(f"Bye, @{ctx.author.name}")


############################## Commands #######################################
    @commands.command(name='help')
    async def help(self, ctx):
        'Maybe could be a usage statement? WIP'
        await ctx.send(f"I can't help you, @{ctx.author.name}")

    @commands.command(name='roll')
    async def roll(self, ctx):
        'Roll a dice. The command arg is the sides of the die.'
        try:
            args = ctx.content.lower().split()
            number = int(args[1])
            await ctx.send(f"@{ctx.author.name} rolled a {random.randint(1,number)}!")
        except:
            await ctx.send(f"Usage: !roll <number>")
    
    @commands.command(name="modLevels")
    async def modLevels(self, ctx):
        'Turns on or off the ability for non-mods to add levels to the queue'
        if ctx.author.is_mod:
            self.canAddLevels = not self.canAddLevels
        else:
            await self._noPerms(ctx)

    @commands.command(name="add")
    async def addLevel(self, ctx):
        'Adds a level code to the queue'
        if self.canAddLevels or ctx.author.is_mod:
            if len(self.levelQueue) < 5:
                args = ctx.content.split()
                code = args[1]
                self.levelQueue.append(code)
                await ctx.send(f"Your level is now in the queue {self.randShoutout(ctx.author.name)}")
            else:
                await ctx.send(f"The level queue is full, try again later {self.randShoutout(ctx.author.name)}")
        else:
            await ctx.send(f"The queue is not currently accepting new levels {self.randShoutout(ctx.author.name)}")

    @commands.command(name="level")
    async def currentLevel(self, ctx):
        'Displays the current level code'
        await self._currentLevel(ctx)
    
    @commands.command(name="nextLevel")
    async def nextLevel(self, ctx):
        'Pops the level off the queue and displays the next value'
        if ctx.author.is_mod:
            if len(self.levelQueue) > 0:
                self.levelQueue.pop(0)
                await self._currentLevel(ctx)
            else:
                await ctx.send(f"The level queue is empty {self.randShoutout(ctx.author.name)}")
        else:
            await self._noPerms(ctx)
    
    @commands.command(name="goodBot")
    async def goodBot(self, ctx):
        'Post a special message to chat'
        await ctx.send(f"{random.choice(self.thanks)} {self.randShoutout(ctx.author.name)}")
    
    @commands.command(name="badBot")
    async def badBot(self, ctx):
        'Post a special message to chat'
        await ctx.send(f"{random.choice(self.jeers)} {self.randShoutout(ctx.author.name)}")
    
    @commands.command(name='cooldown')
    async def setCooldown(self, ctx):
        'Set a new cooldown timer. The command args are number and units.'
        if ctx.author.is_mod:
            args = ctx.content.lower().split()
            number = int(args[1])
            unit = args[2].lower()
            new_time = self.cooldownMgr.updateCooldown(number, unit)
            if new_time is None:
                await ctx.send(f"Usage !cooldown <number> <sec/min/hour>")
            else:
                await ctx.send(f"Set cooldown for {new_time}!")
        else:
            await self._noPerms(ctx)

########################### Misc. Methods #####################################
    async def _currentLevel(self, ctx):
        'Displays the current level code'
        if len(self.levelQueue) > 0:
            await ctx.send(f"Level Code: {self.levelQueue[0]}")
        else:
            await ctx.send(f"The level queue is empty {self.randShoutout(ctx.author.name)}")
    
    async def _noPerms(self, ctx):
        'Called when a user does not have permissions to use a command'
        await ctx.send(f"{random.choice(self.noPerms)} {self.randShoutout(ctx.author.name)}")


if __name__ == "__main__":
    random.seed()
    bot = Bot()
    bot.run()