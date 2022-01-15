# Create your views here.
# -*- coding: utf-8 -*-

from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .gridRecommandationManager import GridChannel

gridChannelClass = GridChannel()


@api_view(["GET"])
@permission_classes([AllowAny])
def getChannels(request):
    return JsonResponse(gridChannelClass.getChannelsByLanguage(), status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def getChannelsProgram(request):
    channelsProgram = [elem for elem in gridChannelClass.getChannelsProgram() if elem is not None]
    return JsonResponse({'programs list': channelsProgram}, status=status.HTTP_200_OK)
