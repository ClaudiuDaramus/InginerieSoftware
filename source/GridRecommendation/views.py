# Create your views here.
# -*- coding: utf-8 -*-

from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .gridManager import GridChannel

gridChannelClass = GridChannel()


@api_view(["GET"])
@permission_classes([AllowAny])
def getChannels(request):
    formattedChannels = gridChannelClass.getChannelsByLanguage()
    # print(formattedChannels)
    # "Jio Cricket English HD": {"id": 430, "lang": 6, "cate": 8}
    return JsonResponse(formattedChannels, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def getChannelsProgram(request):
    formattedChannels = gridChannelClass.getChannelsByLanguage()
    formattedPrograms = gridChannelClass.getChannelsProgram(formattedChannels)
    formattedPrograms = [elem for elem in formattedPrograms if elem is not None]
    # print(formattedPrograms)
    # StreamingHttpResponse

    return JsonResponse({'programs list': formattedPrograms}, status=status.HTTP_200_OK)
