from ..movieAPI.models import VideoContent
from models import *

def addWatchHistory(isLiked,content,profile):
    if content.model is VideoContent:
     addWatchHistory = WatchHistory.objects.create(userId=profile,type=content.model.type,preference=isLiked)
    addWatchHistory.save()