import discord
from discord.ext import commands, tasks
import random
import aiohttp
import json
import datetime

import urllib.parse

from core.database import Database, ProfileInfo

import pathlib


async def random(ctx, name):
    cs = aiohttp.ClientSession()
    async with ctx.channel.typing():
        r = await cs.get(f'https://api.jikan.moe/v4/random/{name}')
        js = await r.json()
        data = js['data']
        await cs.close()

        e = discord.Embed().set_thumbnail(
            url=data["images"]["webp"]["image_url"])
        e.color = 0x4440c0
        e.title = data["title"]
        e.url = data["url"]
        oz = data["synopsis"]
        if oz == None:
            oz = ""
        try:
            oz = oz[:4096]
        except:
            pass
        e.description = f"{oz}"

        for name, value in data.items():

            name = name.replace('_', ' ')
            names = ['mal id', 'url', 'images', 'synopsis', 'titles']
            if value==None or value==False or value==0 or value==True or value==[]:
                pass
            elif name in names:
                pass
            elif isinstance(value, dict):

                try:
                    if value['string'] == None:
                        continue
                    value = f"from {value['string']}"
                    e.add_field(name=name.title(), value=value, inline=True)
                except:
                    continue

            elif isinstance(value, list):
                l = []
                try:
                    for i in range(0, len(value)):
                        z = value[i]['name']
                        l.append(z)

                except:
                    pass
                else:
                    e.add_field(name=name.title(),
                                value=" • ".join(l),
                                inline=True)
                    pass
            else:
                try:
                    value = '{:,}'.format(value)
                except:
                    pass
                e.add_field(name=name.title(), value=value, inline=True)
        await ctx.reply(mention_author=False, embed=e)
        
        
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
    async def dice(self,ctx):
        choice=random.randint(1,6)
        embed = discord.Embed()
        embed.add_field(name="Dice Roll :game_die:",value=f"Rolled a Die and got {choice}. ")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def coin(self,ctx):
        choice=random.choice(["Heads","Tails"])
        embed = discord.Embed()
        embed.add_field(name="Coin Toss :coin:",value=f" Flipped a coin and got {choice}. ")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def weather(self, ctx, *location):
        """Show Weather"""
        queryString = ""
        for local in location: queryString += local + " "

        encodeQueryString = urllib.parse.quote(queryString)
        
        newurl = "https://wttr.in/"+ encodeQueryString + ".png?0?m"

        embed = discord.Embed(color=0xFFFF00)
        embed.set_author(name="Weather Report: {}".format(queryString))
        embed.set_image(url=newurl)

        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def poll(self, ctx, question, *options: str):
        if len(options) <= 1:
            await ctx.send('You need more than one option to make a poll!')
            return
        if len(options) > 10:
            await ctx.send('You cannot make a poll for more than 10 things!')
            return

        if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
            reactions = ['✅', '❌']
        else:
            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)
        embed = discord.Embed(title=question, description=''.join(description))
        react_message = await ctx.send(embed=embed)
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)
        embed.set_footer(text='Poll ID: {}'.format(react_message.id))
        await react_message.edit_message(embed=embed)

    @commands.command(pass_context=True)
    async def tally(self, ctx, id=None):
        poll_message = await ctx.channel.fetch_message(id)
        embed = poll_message.embeds[0]
        unformatted_options = [x.strip() for x in embed.description.split('\n')]
        print(f'unformatted{unformatted_options}')
        opt_dict = {x[:2]: x[3:] for x in unformatted_options} if unformatted_options[0][0] == '1' \
            else {x[:1]: x[2:] for x in unformatted_options}
        # check if we're using numbers for the poll, or x/checkmark, parse accordingly
        voters = [self.bot.user.id]  # add the bot's ID to the list of voters to exclude it's votes

        tally = {x: 0 for x in opt_dict.keys()}
        for reaction in poll_message.reactions:
            if reaction.emoji in opt_dict.keys():
                reactors = await reaction.users().flatten()
                for reactor in reactors:
                    if reactor.id not in voters:
                        tally[reaction.emoji] += 1
                        voters.append(reactor.id)
        output = f"Results of the poll for '{embed.title}':\n" + '\n'.join(['{}: {}'.format(opt_dict[key], tally[key]) for key in tally.keys()])
        await ctx.send(output)
    @commands.command(aliases=['rm', 'rmanga'])
    async def random_manga(self, ctx):
        await random(ctx, 'manga')

    @commands.command(aliases=['ra', 'ranime'])
    async def random_anime(self, ctx):
        await random(ctx, 'anime')
