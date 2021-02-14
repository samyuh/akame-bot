import json
import sys

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                description='Akame Bot', intents=intents)

initial_extensions = ['misc', 'music']

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')

if __name__ == "__main__":
    try:
        with open('config.json') as json_file:
            data = json.load(json_file)
            token = data['token']
    except FileNotFoundError:
        print("Create the file config.json. More information on README.")
        exit()

    for extension in initial_extensions:
        bot.load_extension(extension)

    bot.run(token)