import discord
from discord.ext import commands, tasks

import datetime

import urllib.parse

from core.database import Database, ProfileInfo

import pathlib


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base = Database(None)
        
        # Disable Counter
        # self.timeCounter.start()
        
    @tasks.loop(seconds=60.0)
    async def timeCounter(self):    
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
            
            for userId in memids:
                if userId not in self.base.all_profiles:
                    self.base.all_profiles[userId] = ProfileInfo(self.bot, userId)
                    self.base.insertData(userId)

                self.base.all_profiles[userId].incrementTime()
        
        self.base.updateData()

    @commands.command(pass_context=True)
    async def slides(self, ctx):
        """Get slides"""
        databasePath = str(pathlib.Path().absolute()) + "/main.py"
        await ctx.send(file=discord.File(databasePath))

    @commands.command(pass_context=True)
    async def quote(self, ctx, quote):
        """Set Quote"""
        userId = ctx.message.author.id
        userId = int(userId)

        userInfo = self.bot.get_user(userId)
        if userInfo == None:
            return

        if userId not in self.base.all_profiles:
            self.base.all_profiles[userId] = ProfileInfo(self.bot, userId)
            self.base.insertData(userId)

        profile = self.base.all_profiles[userId]
        profile.quote = quote

        await ctx.send("New quote set!")

    @commands.command(pass_context=True)
    async def profile(self, ctx, user=""):
        """Show profile pic"""
        if user == "":
            userId = ctx.message.author.id
        else:
            userId = user.replace("<@!","")
            userId = userId.replace(">","")

            userId = int(userId)
            print(userId)
            userInfo = self.bot.get_user(userId)
            if userInfo == None:
                return

        if userId not in self.base.all_profiles:
            self.base.all_profiles[userId] = ProfileInfo(self.bot, userId)
            self.base.insertData(userId)

        profile = self.base.all_profiles[userId]
        embed = discord.Embed(color=profile.color)
        embed.set_author(name=profile.name, icon_url=profile.avatar)

        embed.set_image(url=profile.avatar)
        embed.add_field(name="Wise words", value=profile.quote, inline=True)
        # embed.add_field(name="Time Connected", value=profile.timeText, inline=True)
        # embed.add_field(name="Last Appear", value=profile.lastText, inline=True)
        
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def weather(self, ctx, *location):
        """Show Wheater"""
        queryString = ""
        for local in location: queryString += local + " "

        encodeQueryString = urllib.parse.quote(queryString)
        
        newurl = "https://wttr.in/"+ encodeQueryString + ".png?0?m"

        embed = discord.Embed(color=0xFFFF00)
        embed.set_author(name="Weather Report: {}".format(queryString))
        embed.set_image(url=newurl)

        await ctx.send(embed=embed)
