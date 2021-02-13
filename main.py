import json
import sys

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Akame Bot', intents=intents)

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print(bot.get_user(536937288777728002))
    print('\n------')

# Costum Modules
from music.music import Music
from misc.misc import Misc

if __name__ == "__main__":
    with open('config.json') as json_file:
        data = json.load(json_file)
        token = data['token']
        youtubeToken = data['youtubeToken']
    
    bot.add_cog(Music(bot, youtubeToken))
    bot.add_cog(Misc(bot))
    bot.run(token)
