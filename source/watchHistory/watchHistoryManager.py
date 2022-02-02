from movieAPI.models import VideoContent
from .models import *
from tvgrid.models import Channel


def addWatchHistory(isLiked,type,profile,externalId):
    addWatchHistoryObj = WatchHistory.objects.create(profile=profile,type=type,preference=isLiked,externalId=externalId)
    addWatchHistoryObj.save()
    return addWatchHistoryObj
