import pprint

import requests
import json
import os
import datetime
from django.conf import settings
from source.helpers import fromUtcFormat

class TVMazeManager:
    def __init__(self, savePath=settings.BASE_DIR + 'cache/'):
        self.link = settings.TV_MAZE_LINK + 'schedule/full'
        self.savePath = savePath + 'tvMazeFullScheduleLocal.json'

    def acquired(self):
        return os.path.exists(self.savePath)

    def saveData(self):
        try:
            with open(self.savePath, 'w') as tvMazeFile:
                obtainedData = requests.get(self.link)

                if obtainedData.status_code == 200:
                    jsonData = obtainedData.json()
                    tvMazeFile.write(json.dumps(jsonData))
                    return json
                else:
                    raise Exception('%s %s' % (obtainedData.status_code, obtainedData.text))
        except Exception as e:
            raise e

    def readData(self):
        if self.acquired():
            with open(self.savePath) as tvMazeFile:
                readFile = tvMazeFile.read()
                readFile = json.loads(readFile)
                # print(readFile)
                return readFile
        else:
            # raise Exception('This should be saved data')
            return self.saveData()

    def __get__image__(self, image):
        image = image.get('image')

        if image is not None:
            image = image['medium'] if image.get('medium') is not None else image.get('original')
        return image

    def __get__rating__(self, rating):
        rating = rating.get('rating')

        if rating is not None:
            rating = rating.get('average')
        return rating

    def returnAllKeys(self, showList):
        allKeys = []
        for show in showList:
            for key in show:
                if key not in allKeys:
                    allKeys.append(key)
        return allKeys

    def processChannel(self, channel):

        channel, channelType = channel
        country = channel.get('country')
        name = country.get('name') if country is not None else None
        code = country.get('code') if country is not None else None

        return {
            'externalId': int(channel['id']) if channel.get('id') is not None else None,
            'name': channel['name'],
            'country': name,
            'countryCode': code,
            'type': channelType,
        } if channel.get('name') is not None else None

    def processShow(self, entryDictShow):
        # for key in entryDictShow:
        #     print(key, entryDictShow.get(key))

        channel = self.processChannel(
            (entryDictShow['network'], 'tv') if entryDictShow.get('network') is not None
            else (entryDictShow['webChannel'], 'web'))

        return {
            'externalId': int(entryDictShow['id']),
            'name': entryDictShow['name'],
            'language': entryDictShow['language'],
            'genres': entryDictShow['genres'] if entryDictShow['genres'] != [] else None,
            'time': entryDictShow['schedule']['time'] if entryDictShow['schedule']['time'] != '' else None,
            'days': entryDictShow['schedule']['days'],
            'rating': self.__get__rating__(entryDictShow),
            'weight': entryDictShow['weight'],
            'image': self.__get__image__(entryDictShow),
            'channel': channel
        } if entryDictShow['schedule']['days'] != [] else None

    def processScheduled(self, entryScheduled):
        # ["id", "url", "name", "season", "number", "type", "airdate", "airtime", "airstamp",
        #  "runtime", "rating", "image", "summary", "_links", "_embedded"]

        # for key in ["id", "name", "season", "number", "type", "airdate", "airtime", "airstamp",
        #             "runtime", "rating", "image", "_embedded"]:
        #     print(key, entryDict[key])

        startTime = fromUtcFormat(entryScheduled['airstamp'])
        endTime = startTime + datetime.timedelta(minutes=int(entryScheduled['runtime'])) if entryScheduled.get(
            'runtime') is not None else None
        show = self.processShow(entryScheduled['_embedded']['show']) if entryScheduled['_embedded'].get(
            'show') is not None else None

        image = self.__get__image__(entryScheduled)
        rating = self.__get__rating__(entryScheduled)

        if show is not None:
            image = image if image is not None else show['image']
            rating = rating if rating is not None else show['rating']

        return {
            'externalId': int(entryScheduled['id']),
            'name': entryScheduled['name'],
            'season': entryScheduled['season'],
            'number': entryScheduled['number'],
            'startTime': startTime,
            'endTime': endTime,
            'rating': rating,
            'image': image,
            'show': show
        }

    def processedList(self):
        readData = self.readData()
        for show in readData:
            # TODO here we neeed to remap object in format 
            pass

tvMaze = TVMazeManager(os.getcwd())
tvMazeData = tvMaze.readData()
# tvMazeDictKeys = tvMaze.returnAllKeys(tvMazeData)
# print(tvMazeDictKeys)
for show in tvMazeData:
    pprint.pprint(tvMaze.processScheduled(show))
# for key in tvMazeData:
#     print(key)
