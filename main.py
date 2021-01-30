import json

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Akame Bot')

# Costum Modules
from music import *

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')

@bot.command()
async def ping(ctx):
    """Pong"""
    embedVar = discord.Embed(title="Title", description="Desc", color=0x00ff00)
    embedVar.add_field(name="Field1", value="hi", inline=False)
    embedVar.add_field(name="Field2", value="hi2", inline=False)
    await ctx.send(embed=embedVar)

if __name__ == "__main__":
    with open('config.json') as json_file:
        data = json.load(json_file)
        token = data['token']
        youtubeToken = data['youtubeToken']
    
    bot.add_cog(Music(bot, youtubeToken))
    bot.run(token)
