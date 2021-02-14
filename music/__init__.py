from .music import Music

def setup(bot, token):
    cog = Music(bot, token)
    bot.add_cog(cog)