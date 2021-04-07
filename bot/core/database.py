import discord
from discord.ext import commands

import sqlite3

import datetime

class ProfileInfo():
    def __init__(self, bot, userId):
        self.id = userId
        self.bot = bot
        self.user = self.bot.get_user(userId)
        self.name = self.user.display_name
        self.avatar = self.user.avatar_url
        self.color = 0x0099ff
        self.timeText = "Never"
        self.lastText = "Never"
        self.time = 0
    
    def updateTimes(self, timeText, lastText, time):
        self.timeText = timeText
        self.lastText = lastText
        self.time = time

    def incrementTime(self):
        self.time += 0

        minutes_left = self.time

        days = minutes_left // 1440
        minutes_left = minutes_left - days*1440

        hours = minutes_left // 60
        minutes = minutes_left % 60
        
        hours_str = str(hours)
        minutes_str = str(minutes)

        if hours < 10:
            hours_str.zfill(1)
        if minutes < 10:
            minutes_str.zfill(1)

        self.timeText = "{} days, {} hours, {} minutes".format(days, hours_str, minutes_str)

        now = datetime.datetime.now()
        self.lastText = "{}/{}/{} {}:{}".format(now.year, now.month, now.day, now.hour, now.minute)

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self, bot):
        self.all_profiles = {}
        self.conn = sqlite3.connect('./core/database/users.db')

        self.c = self.conn.cursor()

        # Create table
        self.c.execute('''CREATE TABLE IF NOT EXISTS user (
            userId INTEGER PRIMARY KEY,
            timeText VARCHAR(255),
            lastText VARCHAR(255),
            time INTEGER)''')

        lista = self.c.execute("SELECT * FROM user")

        for info in lista: 
            userId = info[0]
            timeText = info[1]
            lastText = info[2]
            time = info[3]

            self.all_profiles[userId] = ProfileInfo(bot, userId)
            self.all_profiles[userId].updateTimes(timeText, lastText, time)

    def insertData(self, key):
        sql = ''' INSERT INTO user VALUES (?, ?, ?, ?)'''

        self.c.execute(sql, (self.all_profiles[key].id, self.all_profiles[key].timeText, self.all_profiles[key].lastText, self.all_profiles[key].time))
        self.conn.commit()

    def updateData(self):
        sql = ''' UPDATE user
                    SET timeText = ? ,
                        lastText = ? ,
                        time = ?
                        WHERE userId = ?'''
        
        for key in self.all_profiles:
            self.c.execute(sql, (self.all_profiles[key].timeText, self.all_profiles[key].lastText, self.all_profiles[key].time, self.all_profiles[key].id))
            self.conn.commit()