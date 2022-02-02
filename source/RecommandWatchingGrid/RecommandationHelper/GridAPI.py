import requests
from rest_framework.response import Response

link = "https://indian-tv-schedule.p.rapidapi.com/"

x_rapidapi_host ="indian-tv-schedule.p.rapidapi.com"
x_rapidapi_key = "92efc58950msh3ba84d45c0ebccfp11e31cjsn09a9ed7db497"

headers = {
    'x-rapidapi-host': x_rapidapi_host,
    'x-rapidapi-key': x_rapidapi_key
}


def getTodaySchedule(channel):
    querystring = {"channel": channel}
    response = requests.request("GET", link + "Schedule", headers=headers, params=querystring)
    print(response.text)

    return Response(response.json())


# print(getTodaySchedule("Jio Cricket Hindi HD"))
