from datetime import datetime, timedelta
from movieAPI.movieManager import oldFormatResponseForInterest, calculateVideoInterestScoreUpgraded
from .models import Episode, Genre
from .serializers import EpisodeSerializer, getOrCreateSimpleBulk, createOrUpdateBasic, ChannelSerializer, \
    ShowSerializer


def formatResponseForInterest(response=None, episodeId=None):
    # print(response)
    if response is None:
        raise Exception('Method needs one parameter')

    oldFormat = oldFormatResponseForInterest(response)
    for key in oldFormat:
        content = oldFormat.pop(key)
        oldFormat[key + "API"] = content

    if episodeId is not None:
        episode = Episode.objects.get(id=episodeId).getJSONVariant()
        oldFormat.update({
            'rating': episode['rating'],
            'show': episode['show']['name'],
            'language': episode['show']['language'],
            'channel': episode['show']['channel']['name'],
            'channelType': episode['show']['channel']['type'],
            'startTime': episode['startTime'],
            'endTime': episode['endTime'],
        })

    return oldFormat


def getScheduleEpisodes():
    todayDatetime = datetime.combine(datetime.today(), datetime.min.time())
    print(todayDatetime, todayDatetime + timedelta(days=2))
    episodes = Episode.objects.filter(startTime__gte=todayDatetime, startTime__lte=todayDatetime + timedelta(days=2)) \
        .order_by('endTime', 'startTime')
    return [episode.getJSONVariant() for episode in episodes]


def updateTVScheduleObject(schedule):
    show = schedule['show']

    # they already are in the database
    getOrCreateSimpleBulk(Genre, show['genres'])

    channel = show['channel']
    channelObject = createOrUpdateBasic(ChannelSerializer, channel, (True, False))
    # print('Channel id %s' % channelObject.id)
    show['channel'] = channelObject
    showObject = createOrUpdateBasic(ShowSerializer, show, (True, False), ['genres', 'days', 'channel'])
    # print(showObject)
    # print('Show id %s' % showObject.id)
    # print(showObject)
    schedule['show'] = showObject
    episodeObject = createOrUpdateBasic(EpisodeSerializer, schedule, (True, True), ['show'])

    return episodeObject.getJSONVariant()
