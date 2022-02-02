from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
import json
import os
from uuid import uuid4

import requests
from django.contrib.auth import authenticate

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.http import StreamingHttpResponse

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token

from django.shortcuts import render, get_object_or_404, get_list_or_404

from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins

from rest_framework import status

from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django.contrib.auth.models import User

from .tvGridManager import tvManager
from .serializers import *


def renderTVScheduleObjects():
    processedScheduleList = tvManager.processedList()
    getOrCreateSimpleBulk(Day, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    for schedule in processedScheduleList:
        yield updateTVScheduleObject(schedule)


def updateTVScheduleObject(schedule):
    show = schedule['show']

    # they already are in the database
    # getOrCreateSimpleBulk(Genre, show['genres'])

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


from datetime import datetime, timedelta

def getScheduleEpisodes():
    todayDatetime = datetime.combine(datetime.today(), datetime.min.time())
    print(todayDatetime, todayDatetime + timedelta(days=2))
    episodes = Episode.objects.filter(startTime__gte=todayDatetime, startTime__lte=todayDatetime + timedelta(days=2)) \
        .order_by('startTime', 'endTime')
    return [episode.getJSONVariant() for episode in episodes]

@api_view(['GET'])
@permission_classes([IsAdminUser])
def viewSchedule(request):
    episodes = getScheduleEpisodes()

    return Response({"result": episodes}, )

