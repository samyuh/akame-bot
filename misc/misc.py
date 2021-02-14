import discord
from discord.ext import commands, tasks

import datetime

all_profiles = {}

class ProfileInfo():
    def __init__(self, user):
        self.time = 1000
        self.avatar = user.avatar_url
        self.name = user.display_name
        self.color = 0x0099ff
        self.timeText = "Never"
        self.lastText = "Never"
        self.time = 0
    
    def incrementTime(self):
        self.time += 1

        minutes_left = self.time

        days = minutes_left // 1440
        minutes_left = minutes_left - days*1440

        hours = minutes_left // 60
        minutes = minutes_left % 60

        self.timeText = "{} days, {} hours, {} minutes".format(days, hours, minutes)

        now = datetime.datetime.now()
        self.lastText = "{}/{}/{} {}:{}".format(now.year, now.month, now.day, now.hour, now.minute)


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.printer.start()
    
    @tasks.loop(seconds=60.0)
    async def printer(self):
        guild = self.bot.get_guild(700343486897061991)
        if guild != None:
            voice_channel_list = guild.voice_channels
            voice_channels_ids = []

            memids = []

            for voice_c in voice_channel_list:
                voice_channels_ids.append(voice_c.id)
                members = voice_c.members

                for member in members:
                    memids.append(member.id)

            for i in memids:
                userInfo = self.bot.get_user(i)
                if userInfo not in all_profiles:
                    all_profiles[userInfo] = ProfileInfo(userInfo)

                all_profiles[userInfo].incrementTime()


    @commands.command(pass_context=True)
    async def profile(self, ctx, user=""):
        """Show profile pic"""
        if user == "":
            userInfo = ctx.message.author
        else:
            print(user)
            user = user.replace("<@!","")
            user = user.replace(">","")

            userInfo = self.bot.get_user(int(user))
            print(userInfo)
            if userInfo == None:
                return

        if userInfo not in all_profiles:
            all_profiles[userInfo] = ProfileInfo(userInfo)

        profile = all_profiles[userInfo]
        print(profile.avatar)

        embed = discord.Embed(color=profile.color)
        embed.set_author(name=profile.name, icon_url=profile.avatar)

        embed.set_image(url=profile.avatar)
        embed.add_field(name="Time Connected", value=profile.timeText, inline=True)
        embed.add_field(name="Last Appear", value=profile.lastText, inline=True)
        
        await ctx.send(embed=embed)