import json
import sys

import discord
from discord.ext import commands

# Costum Modules
from music import setup as musicSetup, Music
from misc import setup as miscSetup, Misc

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                description='Akame Bot', intents=intents)

class Akame():
    def __init__(self, bot):
        self.bot = bot
        
        self.profiles = {}

        with open('config.json') as json_file:
            data = json.load(json_file)
            self.token = data['token']
            self.youtubeToken = data['youtubeToken']

        musicSetup(self.bot, self.youtubeToken)
        miscSetup(self.bot)
        bot.run(self.token)

    @bot.event
    async def on_ready():
        print('Logged in as {0} ({0.id})'.format(bot.user))
        print(bot.get_user(536937288777728002))
        print('\n------')

if __name__ == "__main__":
    start = Akame(bot)