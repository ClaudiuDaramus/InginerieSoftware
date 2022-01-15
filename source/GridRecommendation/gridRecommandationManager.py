import json

import requests
from django.conf import settings


class GridChannel:
    def __init__(self):
        self.channels = settings.CHANNELS
        self.televisSettings = settings.TEL_SETTINGS
        self.userHistory = settings.USER_HIST
        self.headers = {
            'x-rapidapi-host': settings.INDIAN_TV_SCHEDULE_HOST,
            'x-rapidapi-key': settings.INDIAN_TV_SCHEDULE_KEY,
        }

    def getChannelsByLanguage(self, langList=None):
        if langList is None:
            langList = ['English']
        langList = [self.televisSettings['languages'].get(lang, "no language") for lang in langList]
        channelDict = {}
        for key in self.channels:
            channel = self.channels[key]
            if channel['lang'] in langList:
                channelDict[key] = channel
        return channelDict

    def getChannelsProgram(self):
        channels = self.getChannelsByLanguage()
        return [{
            'channel': key,
            'program': self.getTodaySchedule(key)
        } for key in channels]

    def getTodaySchedule(self, channel):
        querystring = {"channel": channel}
        response = requests.request("GET", settings.INDIAN_TV_SCHEDULE_LINK + "Schedule", headers=self.headers, params=querystring)
        # print(response.text)
        if response.status_code == 200:
            return response.json()
        else:
            return None

# gch = GridChannel()
# print(gch.getChannelsByLanguage())
