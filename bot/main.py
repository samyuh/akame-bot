import json
import sys

import discord
from discord.ext import commands

from core.database import Database
import sqlite3

import datetime

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                description='Akame Bot', intents=intents)

initial_extensions = ['misc']

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('---------')

    print('Init Database')
    database = Database(bot)

    for extension in initial_extensions:
        print('Loaded Extension: {}'.format(extension))
        bot.load_extension(extension)

if __name__ == "__main__":
    try:
        with open('config.json') as json_file:
            data = json.load(json_file)
            token = data['token']
    except FileNotFoundError:
        print("Create the file config.json. More information on README.")
        exit()

    bot.run(token)