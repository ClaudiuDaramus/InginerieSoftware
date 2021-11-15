from django.shortcuts import render
# Create your views here.
import requests

link = "https://indian-tv-schedule.p.rapidapi.com/"

headers = {
    'x-rapidapi-host': "indian-tv-schedule.p.rapidapi.com",
    'x-rapidapi-key': "92efc58950msh3ba84d45c0ebccfp11e31cjsn09a9ed7db497"
}


def getCategories():
    response = requests.request("GET", link + "get-categories", headers=headers)
    print(response.text)

    return response.text


def getTodaySchedule(channel):
    querystring = {"channel": channel}
    response = requests.request("GET", link + "today-schedule", headers=headers, params=querystring)
    print(response.text)

    return response.text


def getSchedule(channel):
    querystring = {"channel": channel}
    response = requests.request("GET", link + "chedule", headers=headers, params=querystring)
    print(response.text)

    return response.text


def getSearchChannel(lang, cate):
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