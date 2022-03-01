class ProfileInfo():
    def __init__(self, bot, userId):
        self.id = userId
        self.bot = bot
        self.user = self.bot.get_user(userId)
        self.name = self.user.display_name
        self.avatar = self.user.avatar_url
        self.quote = "None"
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