import discord
from discord.ext import commands

import sqlite3

import datetime

from .profile import ProfileInfo

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
        self.conn = sqlite3.connect('../database/users.db')

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