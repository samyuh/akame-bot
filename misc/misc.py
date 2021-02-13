import discord
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def profile(self, ctx, user=""):
        """Show profile pic"""
        if user == "":
            profilePic = ctx.message.author.avatar_url
        else:
            user = user.replace("<","")
            user = user.replace(">","")
            user = user.replace("@!","")

            userValue = self.bot.get_user(int(user))
            profilePic = userValue.avatar_url

        embed = discord.Embed()
        embed.set_image(url=profilePic)

        await ctx.send(embed=embed)