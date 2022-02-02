import rest_framework.decorators
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
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token

from django.shortcuts import render, get_object_or_404, get_list_or_404

from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.decorators import renderer_classes
from rest_framework import generics
from rest_framework import mixins
from rest_framework.settings import api_settings

from rest_framework import status

from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .models import *
from authentication.models import Profile
from random import randint, choices
from .watchHistoryManager import addWatchHistory
from tvgrid.models import *
@api_view(["GET"])
@permission_classes([AllowAny])
def createHistory(request):
    isLiked = request.GET.get("isLiked")
    if isLiked.lower() == "true":
        isLiked = True
    elif isLiked.lower() == "false":
        isLiked = False
    else:
        isLiked = True
        # default

    print(isLiked)
    type = request.GET.get("type", "VideoContent")
    profileName = request.GET.get("profileName")
    profile = Profile.objects.filter(profileName=profileName).filter(user__id=request.user.id).first()
    externalId = request.GET.get("externalId", 0)
    if profile is None:
        return JsonResponse({"error":"There is no profile with this name"})
    history = addWatchHistory(isLiked = isLiked, type = type, profile = profile, externalId = externalId )
    return JsonResponse(history.getJSONVariant())

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def createAutomatedHistory(request):
 episodes = Episode.objects.all()
 episodesId = [episode.id for episode in episodes]
 episodesId= choices(episodesId, k=20)
 return JsonResponse({"results":episodesId})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def findProfile(request):
    profileName = request.GET.get("default ")
    return JsonResponse(profileName.getJsonVariant())