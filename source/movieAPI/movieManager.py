import urllib.parse

import requests
import urllib3
from django.conf import settings

mainLink = settings.OMDB_LINK
omdbKey = settings.OMDB_KEY

# always add percentageSum
videoInterest = {
    'rated': (0, 0.2),
    'director': (0, 0.3),
    'type': (0, 0.1),
    'genres': (1, 0.3),
    'actors': (1, 0.5),
    'languages': (1, 0.05),
    'countries': (1, 0.05),
    'production': (1, 0.3),
    'writers': (1, 0.5),
    'runtime': (2, 0.1),
    'percentageSum': 2.4
}


# we want to return name, id and poster for element variants
def bigSearchForVideoContent(title=None):
    if title is None:
        raise Exception('Method needs at least one parameter')

    page = 1
    parameters = urllib.parse.urlencode({'apiKey': omdbKey, 's': title, 'page': page})
    response = requests.get(mainLink + parameters).json()

    movieTitlesList = []
    while response['Response'] == 'True':
        page += 1
        for film in response['Search']:
            movieTitlesList.append((film['Title'], film['imdbID'], None if film['Poster'] == 'N/A' else film['Poster']))

        parameters = urllib.parse.urlencode({'apiKey': omdbKey, 's': title, 'page': page})
        response = requests.get(mainLink + parameters).json()

    return movieTitlesList


def searchForVideoContent(imdbID=None, title=None, plotType='full'):
    if imdbID is None and title is None:
        raise Exception('Method needs at least one parameter')

    searchBy = ('i', imdbID) if imdbID is not None else ('t', title)
    parameters = urllib.parse.urlencode({'apiKey': omdbKey, searchBy[0]: searchBy[1], 'plot': plotType})
    response = requests.get(mainLink + parameters).json()
    print(response)
    response = formatResponse(response)
    response["Response"] = 'True'
    return None if response['Response'] == 'False' else response


def formatResponseForInterest(response=None):
    # print(response)
    if response is None:
        raise Exception('Method needs one parameter')
    return {
        'rated': response['Rated'],
        'runtime': int(response['Runtime'].split(' min')[0]) if response['Runtime'] != 'N/A' else None,
        'genres': [elem.lower() for elem in response['Genre'].split(', ')],
        'director': response['Director'] if response['Director'] != 'N/A' else [],
        'writers': [elem.lower() for elem in response['Writer'].split(', ') if elem != 'N/A'],
        'actors': [elem.lower() for elem in response['Actors'].split(', ')],
        'languages': [elem.lower() for elem in response['Language'].split(', ')],
        'countries': [elem.lower() for elem in response['Country'].split(', ')],
        'type': response['Type'],
        'production': [elem.lower() for elem in response['Production'].split(', ')]
        if response.get('Production') and response.get('Production') != 'N/A' else []
    }
def formatResponse(response=None):

    if response is None:
        raise Exception('Method needs one parameter')
    else:
        imdbID = response['imdbID']
        response = formatResponseForInterest(response)
        response['imdbID'] = imdbID
        return response

def calculateVideoInterestScoreUpgraded(firstFilmList=None, secondFilmList=None):
    if firstFilmList is None or secondFilmList is None:
        raise Exception('Method need both parameters')

    interestListScore = {}
    for firstFilm in firstFilmList:
        for secondFilm in secondFilmList:
            for key in videoInterest:
                if key != 'percentageSum':
                    (videoObjectType, videObjectWeight) = videoInterest[key]
                    if videoObjectType == 0:
                        # print(firstFilm[key])
                        interestListScore[key] = 1 if firstFilm[key] == secondFilm[key] else 0

                    elif videoObjectType == 1:
                        counter = 0
                        for firstElem in firstFilm[key]:
                            if firstElem in secondFilm[key]:
                                counter += 1

                        maxLength = max(len(firstFilm[key]), len(secondFilm[key]))
                        interestListScore[key] = 0 if maxLength == 0 else 1.0 * counter / maxLength

                    elif videoObjectType == 2:
                        if firstFilm[key] is None or secondFilm[key] is None:
                            interestListScore[key] = 0
                        else:
                            minLength = min(firstFilm[key], secondFilm[key]) * 1.0
                            maxLength = max(firstFilm[key], secondFilm[key]) * 1.0

                            interestListScore[key] = 0 if maxLength == 0 else 1.0 * minLength / maxLength

    interestValue = 0
    for key in videoInterest:
        if key != 'percentageSum':
            (videoType, videoWeight) = videoInterest[key]
            interestListScore[key] = round((interestListScore[key] * 100), 2)
            interestValue += interestListScore[key] * videoWeight / videoInterest['percentageSum']

    return interestListScore, round(interestValue, 2)

# filmList = bigSearchForVideoContent('alchemist')
#
# print(len(filmList))
# print(filmList)

# print(searchForVideoContent(title='Shadowhunters: The Mortal Instruments'))

# firstUserSearch = searchForVideoContent(title='avatar')
# secondUserSearch = searchForVideoContent(title='the last airbender')
#
# print(firstUserSearch)
# firstSearchFormatted = formatResponseForInterest(firstUserSearch)
# secondSearchFormatted = formatResponseForInterest(secondUserSearch)
#
# print(firstSearchFormatted, secondSearchFormatted)
# print(calculateVideoInterestScore([firstSearchFormatted], [secondSearchFormatted]))