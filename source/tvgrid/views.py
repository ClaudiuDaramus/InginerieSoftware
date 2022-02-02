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
from movieAPI.movieManager import searchForVideoContent, formatResponseForInterest, calculateVideoInterestScoreUpgraded
from recommandationHelper import WeightedIntervalScheduling


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def compareMovieListView(request):
    firstMovieList = request.GET.get('firstList')
    firstMovieList = None if firstMovieList is None else firstMovieList.split(',')
    firstMovieIDList = request.GET.get('firstIdList')
    firstMovieIDList = None if firstMovieIDList is None else firstMovieIDList.split(',')
    secondMovieList = request.GET.get('secondList')
    secondMovieList = None if secondMovieList is None else secondMovieList.split(',')
    secondMovieIDList = request.GET.get('secondIdList')
    secondMovieIDList = None if secondMovieIDList is None else secondMovieIDList.split(',')

    try:
        if firstMovieList is not None:
            firstMovieList = [searchForVideoContent(title=movie) for movie in firstMovieList]
        else:
            firstMovieList = []

        if firstMovieIDList is not None:
            for movieID in firstMovieIDList:
                firstMovieList.append(searchForVideoContent(imdbID=movieID))

        if secondMovieList is not None:
            secondMovieList = [searchForVideoContent(title=movie) for movie in secondMovieList]
        else:
            secondMovieList = []

        if secondMovieIDList is not None:
            for movieID in secondMovieIDList:
                secondMovieList.append(searchForVideoContent(imdbID=movieID))

        # elem1 = [movie['Runtime'] for movie in firstMovieList]
        # elem2 = [movie['Runtime'] for movie in secondMovieList]
        # print(elem1)
        # print(elem2)

        firstMovieList = [formatResponseForInterest(movie) for movie in firstMovieList]
        secondMovieList = [formatResponseForInterest(movie) for movie in secondMovieList]
        # print(firstMovieList, secondMovieList)
        # firstMovieList should be the schedule received from url('schedule/', viewSchedule, name='schedule') in tvgrid
        # secondMovieList should be the watchHistory, for now use a dummy one
        scheduleListWeighted = calculateVideoInterestScoreUpgraded(firstMovieList, secondMovieList)
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
