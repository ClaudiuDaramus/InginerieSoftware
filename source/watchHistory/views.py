# Create your views here.
# -*- coding: utf-8 -*-

from random import choices, randint

from authentication.models import Profile
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from tvgrid.models import *

from .watchHistoryManager import addWatchHistory


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
        return JsonResponse({"error": "There is no profile with this name"})
    history = addWatchHistory(isLiked=isLiked, type=type, profile=profile, externalId=externalId)
    return JsonResponse(history.getJSONVariant())


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def createAutomatedHistory(request):
    profileName = request.GET.get("profileName", "default")
    print(request.user)
    profile = Profile.objects.filter(profileName=profileName, user=request.user).first()

    if profile is None:
        return JsonResponse({"errors": "There is no profile"})

    episodes = Episode.objects.all()
    episodesId = [episode.id for episode in episodes]
    # print(episodesId)
    episodesId = choices(episodesId, k=20)
    # isLiked, type, profile, externalId

    isLiked = True if randint(0, 12) % 2 == 1 else False
    historyCreated = [addWatchHistory(isLiked, "tv", profile, epId).getJSONVariant() for epId in episodesId]
    return JsonResponse({"results": historyCreated})
