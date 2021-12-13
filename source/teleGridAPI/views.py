from django.shortcuts import render
# Create your views here.
import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from source.settings import x_rapidapi_host, x_rapidapi_key

link = "https://indian-tv-schedule.p.rapidapi.com/"

headers = {
    'x-rapidapi-host': x_rapidapi_host,
    'x-rapidapi-key': x_rapidapi_key
}

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCategories(request):
    response = requests.get(link + "getCategories", headers=headers)
    print(response.text)

    return Response(response.json())

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getTodaySchedule(request):
    channel = request.GET.get("channel")
    querystring = {"channel": channel}
    response = requests.request("GET", link + "Schedule", headers=headers, params=querystring)
    print(response.text)

    return Response(response.json())

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSchedule(request, channel):
    querystring = {"channel": channel}
    response = requests.request("GET", link + "chedule", headers=headers, params=querystring)
    print(response.text)

    return response.text

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSearchChannel(request, lang, cate):
    querystring = {}
    if lang & cate:
        querystring = {"lang": lang, "cate": cate}
    elif lang:
        querystring = {"lang": lang}
    elif cate:
        querystring = {"cate": cate}
    response = requests.request("GET", link + "search-channel", headers=headers, params=querystring)
    print(response.text)

    return response.text