# Create your views here.
# -*- coding: utf-8 -*-

from django.http import HttpResponse, JsonResponse
from django.http import StreamingHttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .scheduleHelper import getScheduleEpisodes, updateTVScheduleObject
from .serializers import *
from .tvGridManager import tvManager
from movieAPI.movieManager import searchForVideoContent, calculateVideoInterestScoreUpgraded
from .recommandationHelper import WeightedIntervalScheduling
from .scheduleHelper import formatResponseForInterest
from watchHistory.models import WatchHistory
from authentication.models import Profile

def renderTVScheduleObjects():
    processedScheduleList = tvManager.processedList()
    getOrCreateSimpleBulk(Day, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    for schedule in processedScheduleList:
        yield updateTVScheduleObject(schedule)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def updateTVSchedule(request):
    return StreamingHttpResponse(renderTVScheduleObjects())


@api_view(['GET'])
@permission_classes([IsAdminUser])
def functionTesting(request):
    channel = Channel.objects.filter(countryCode='US').all()
    print(channel)
    shows = Show.objects.filter(channel__in=channel).all()
    print(shows)
    for show in shows:
        print(show.getJSONVariant())
    return HttpResponse({'result': ''})
    # pass


@api_view(['GET'])
@permission_classes([IsAdminUser])
def viewSchedule(request):
    episodes = getScheduleEpisodes()
    return Response({"result": episodes}, )


def searchableShowContent(jsonList):
    watchHistoryDict = {}
    for index, watched in enumerate(jsonList):
        watchHistoryDict[watched['id']] = (searchForVideoContent(title=watched['show']['name']), index)

    newWatchHistoryDict = {}
    for key in watchHistoryDict:
        if watchHistoryDict.get(key)[0] is not None:
            newWatchHistoryDict[key] = watchHistoryDict[key]

    return newWatchHistoryDict

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def compareMovieListView(request):

    profileName = request.GET.get("profileName")
    if profileName is None:
        return JsonResponse({"errors": "You need to complete the profile name parameter"})
    # get Profile using profile obj and name from request
    profile = Profile.objects.filter(profileName=profileName).filter(user__id=request.user.id).first()
    watchHistory = WatchHistory.objects.filter(profile=profile, type="tv").all()
    watchHistory = Episode.objects.filter(id__in=[watched.externalId for watched in watchHistory]).all()
    watchHistory = [watched.getJSONVariant() for watched in watchHistory]
    # return JsonResponse(watchHistory, safe=False)
    episodes = getScheduleEpisodes()
    # return JsonResponse(episodes, safe=False)

    watchHistoryDict = searchableShowContent(watchHistory)
    episodeDict = searchableShowContent(episodes)
    
    try:
        watchHistoryList = [formatResponseForInterest(watchHistoryDict[key][0], watchHistory[watchHistoryDict[key][1]]) for key in watchHistoryDict]
        episodeList = [formatResponseForInterest(episodeDict[key][0], episodes[episodeDict[key][1]]) for key in episodeDict]

        scheduleListWeighted = calculateVideoInterestScoreUpgraded(watchHistoryList, episodeList)
        # scheduleListWeighted has tuples of all the entries from the schedule received paired with their respective
        # interest

        reformattedListForWeightedIntervalScheduling = []
        for i in range(len(scheduleListWeighted)):
            # scheduleListWeighted[X][0] is the entry/episode at index X in scheduleListWeighted \
            # scheduleListWeighted[X][1] is the entry/episode's interest at index X in scheduleListWeighted
            reformattedListForWeightedIntervalScheduling.append((scheduleListWeighted[i][0]["startTime"],
                                                                 scheduleListWeighted[i][0]["endTime"],
                                                                 scheduleListWeighted[i][1], i))

        weightedInterval = WeightedIntervalScheduling(reformattedListForWeightedIntervalScheduling)
        max_weight, best_intervals = weightedInterval.weighted_interval()
        bestSchedule = []
        for elem in best_intervals:
            # elem[3] = scheduleListWeighted index
            # scheduleListWeighted[X][0] is the entry/episode at index X in scheduleListWeighted
            bestSchedule.append(scheduleListWeighted[elem[3]][0])
        return JsonResponse({'results': bestSchedule})

    except Exception as e:
        return JsonResponse({'error': str(e)})
