# Create your views here.
# -*- coding: utf-8 -*-

from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from tvgrid.recommandationHelper import WeightedIntervalScheduling
from .movieManager import bigSearchForVideoContent, formatResponseForInterest, searchForVideoContent, \
    calculateVideoInterestScoreUpgraded


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def searchForMovieView(request):
    title = request.GET.get('title')

    try:
        search = bigSearchForVideoContent(title)
        return JsonResponse({'results': search})
    except Exception as e:
        return JsonResponse({'error': str(e)})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def findMovieView(request):
    title = request.GET.get('title')
    imdbId = request.GET.get('imdbId')
    # there is an error here i think idk what to do
    try:
        search = searchForVideoContent(imdbId, title)
        # search = formatResponseForInterest(search)
        return JsonResponse({'results': search})
    except Exception as e:
        return JsonResponse({'error': str(e)})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def compareMoviesView(request):
    firstMovie = request.GET.get('firstTitle')
    firstMovieID = request.GET.get('firstImdbId')
    secondMovie = request.GET.get('secondTitle')
    secondMovieID = request.GET.get('secondImdbId')

    try:
        firstMovie = searchForVideoContent(imdbID=firstMovieID, title=firstMovie)
        secondMovie = searchForVideoContent(imdbID=secondMovieID, title=secondMovie)

        firstMovieFormatted = formatResponseForInterest(firstMovie)
        secondMovieFormatted = formatResponseForInterest(secondMovie)

        interest = calculateVideoInterestScoreUpgraded([firstMovieFormatted], [secondMovieFormatted])
        return JsonResponse({'results': interest})

    except Exception as e:
        return JsonResponse({'error': str(e)})


# Find the latest job (in sorted array) that
# doesn't conflict with the job[i]. If there
# is no compatible job, then it returns -1
def latestNonConflict(arr, i):
    for j in range(i - 1, -1, -1):
        if arr[j][0]["endTime"] <= arr[i - 1][0]["startTime"]:
            return j

    return -1


# A recursive function that returns the
# maximum possible profit from given
# array of jobs. The array of jobs must
# be sorted according to finish time
def findMaxProfitRec(scheduleListWeighted, n, scheduleList=[]):
    # pass scheduleListWeighted from compareMovieListView
    # originally, n = len(compareMovieListViewResult['results'])
    # entry = scheduleListWeighted[X][0], entryInterest = scheduleListWeighted[X][1]

    # Base case
    if n == 1:
        scheduleList.append(scheduleListWeighted[n - 1][0])
        return scheduleListWeighted[n - 1][1]

    # Find profit when current job is included
    inclProf = scheduleListWeighted[n - 1][1]
    i = latestNonConflict(scheduleListWeighted, n)

    if i != -1:
        inclProf += findMaxProfitRec(scheduleListWeighted, i + 1)

    # Find profit when current job is excluded
    exclProf = findMaxProfitRec(scheduleListWeighted, n - 1)
    return max(inclProf, exclProf)


