from .misc import Misc

def setup(bot):
    cog = Misc(bot)
    bot.add_cog(cog)