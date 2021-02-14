import json
from .music import Music

with open('config.json') as json_file:
    data = json.load(json_file)
    token = data['youtubeToken']

def setup(bot):
    cog = Music(bot, token)
    bot.add_cog(cog)