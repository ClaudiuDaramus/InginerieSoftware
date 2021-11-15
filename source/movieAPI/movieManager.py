import urllib.parse

import requests
import urllib3
from django.conf import settings

# settings.configure()

mainLink = settings.OMDB_LINK
omdbKey = settings.OMDB_KEY

videoInterestKeys = [('rated', 0), ('director', 0), ('type', 0), ('genres', 1), ('actors', 1), ('languages', 1),
                     ('countries', 1), ('production', 1), ('writers', 1), ('runtime', 2)]

percentageInterestKeys = [('rated', 0.2), ('director', 0.3), ('type', 0.1), ('genres', 0.3), ('actors', 0.5),
                          ('languages', 0.05), ('countries', 0.05), ('production', 0.3), ('writers', 0.5),
                          ('runtime', 0.1)]
percentageSum = 2.4


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
    return None if response['Response'] == 'False' else response


def formatResponseForInterest(response=None):
    if response is None:
        raise Exception('Method needs one parameter')

    return {
        'rated': response['Rated'],
        'runtime': int(response['Runtime'].split(' min')[0]),
        'genres': [elem.lower() for elem in response['Genre'].split(',')],
        'director': response['Director'],
        'writers': [elem.lower() for elem in response['Writer'].split(',')],
        'actors': [elem.lower() for elem in response['Actors'].split(',')],
        'languages': [elem.lower() for elem in response['Language'].split(',')],
        'countries': [elem.lower() for elem in response['Country'].split(',')],
        'type': response['Type'],
        'production': [elem.lower() for elem in response['Production'].split(',')] if response.get('Production') else []
    }


def calculateVideoInterestScore(firstFilmList=None, secondFilmList=None):
    if firstFilmList is None or secondFilmList is None:
        raise Exception('Method need both parameters')

    interestListScore = {}
    for firstFilm in firstFilmList:
        for secondFilm in secondFilmList:
            for (key, isSimple) in videoInterestKeys:
                if isSimple == 0:
                    if firstFilm[key] == secondFilm[key]:
                        interestListScore[key] = 1
                    else:
                        interestListScore[key] = 0
                elif isSimple == 1:
                    counter = 0
                    for firstElem in firstFilm[key]:
                        if firstElem in secondFilm[key]:
                            counter += 1
                    interestListScore[key] = 1.0 * counter / max(len(firstFilm[key]), len(secondFilm[key]))
                elif isSimple == 2:
                    minLength = min(firstFilm[key], secondFilm[key]) * 1.0
                    maxLength = max(firstFilm[key], secondFilm[key]) * 1.0

                    interestListScore[key] = minLength / maxLength

    interestValue = 0
    for key, score in percentageInterestKeys:
        interestValue += interestListScore[key] * score

    return interestListScore, interestValue / percentageSum


filmList = bigSearchForVideoContent('alchemist')

print(len(filmList))
print(filmList)

print(searchForVideoContent(title='Shadowhunters: The Mortal Instruments'))

firstUserSearch = searchForVideoContent(title='avatar')
secondUserSearch = searchForVideoContent(title='the last airbender')

print(firstUserSearch)
firstSearchFormatted = formatResponseForInterest(firstUserSearch)
secondSearchFormatted = formatResponseForInterest(secondUserSearch)

print(firstSearchFormatted, secondSearchFormatted)
print(calculateVideoInterestScore([firstSearchFormatted], [secondSearchFormatted]))
