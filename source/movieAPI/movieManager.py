import urllib.parse

import requests
import urllib3
from django.conf import settings

mainLink = settings.OMDB_LINK
omdbKey = settings.OMDB_KEY

# always add percentageSum
oldVideoInterest = {
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

videoInterest = {
    'ratedAPI': (0, 7.2),
    'directorAPI': (0, 7.8),
    'typeAPI': (0, 3.6),
    'genresAPI': (1, 14.4),
    'actorsAPI': (1, 12.0),
    'languagesAPI': (1, 1.8),
    'countriesAPI': (1, 1.8),
    'productionAPI': (1, 10.8),
    'writersAPI': (1, 9.0),
    'runtimeAPI': (2, 3.6),
    'imdbRatingAPI': (0, 12.0),
    'metascoreAPI': (0, 6.0),
    'rating': (0, 2.5),
    'show': (0, 4.0),
    'language': (0, 2.0),
    'channel': (0, 0.2),
    'channelType': (0, 1.3)
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
    return None if response['Response'] == 'False' else response


def oldFormatResponseForInterest(response=None):
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
        'imdbRating': float(response['imdbRating']),
        'metascore': float(response['Metascore']),
        'type': response['Type'],
        'production': [elem.lower() for elem in response['Production'].split(', ')]
        if response.get('Production') and response.get('Production') != 'N/A' else []
    }

    # return {
    #     # rating, sameShow, showRating, showLanguage, sameChannel(channelName), channelType if show is found by API
    #     # in findMovieView, add: year, genre, director, writer, actors, languages, country, imdbRating, type
    #     'rating': response['rating'],
    #     'show': response['show']['name'],
    #     'language': response['show']['language'],
    #     'channel': response['show']['channel']['name'],
    #     'channelType': response['show']['channel']['type'],
    #     'startTime': response['startTime'],
    #     'endTime': response['endTime'],
    #     'ratedAPI': response['Rated'],
    #     'runtimeAPI': int(response['Runtime'].split(' min')[0]) if response['Runtime'] != 'N/A' else None,
    #     'genresAPI': [elem.lower() for elem in response['Genre'].split(', ')],
    #     'directorAPI': response['Director'] if response['Director'] != 'N/A' else [],
    #     'writersAPI': [elem.lower() for elem in response['Writer'].split(', ') if elem != 'N/A'],
    #     'actorsAPI': [elem.lower() for elem in response['Actors'].split(', ')],
    #     'languagesAPI': [elem.lower() for elem in response['Language'].split(', ')],
    #     'countriesAPI': [elem.lower() for elem in response['Country'].split(', ')],
    #     'imdbRatingAPI': float(response['imdbRating']),
    #     'metascoreAPI': float(response['Metascore']),
    #     'typeAPI': response['Type'],
    #     'productionAPI': [elem.lower() for elem in response['Production'].split(', ')]
    #     if response.get('Production') and response.get('Production') != 'N/A' else []
    # }


def calculateVideoInterestScoreUpgraded(schedule=None, watchHistory=None):
    # first list should be the unsorted schedule, the second list the watch history

    if schedule is None or watchHistory is None:
        raise Exception('Method need both parameters')

    # every entry in the schedule list will be weighted by the interest (in relation to the watchHistory)
    scheduleListWeighted = []
    for i in len(schedule):
        episode = schedule[i]
        for entry in watchHistory:
            percentageSum = 100
            interestValue = 0
            for key in videoInterest:
                (videoObjectType, videoObjectWeight) = videoInterest[key]
                if episode[key] is None or entry[key] is None:
                    percentageSum -= videoObjectWeight
                elif videoObjectType == 0:
                    interestValue += videoObjectWeight if episode[key] == entry[key] else 0

                elif videoObjectType == 1:
                    counter = 0
                    for firstElem in episode[key]:
                        if firstElem in entry[key]:
                            counter += 1

                    maxLength = max(len(episode[key]), len(entry[key]))
                    interestValue += 0 if maxLength == 0 else videoObjectWeight * counter / maxLength

                elif videoObjectType == 2:
                    minLength = min(episode[key], entry[key]) * 1.0
                    maxLength = max(episode[key], entry[key]) * 1.0

                    interestValue += 0 if maxLength == 0 else videoObjectWeight * minLength / maxLength

            episodeInterest = round(interestValue / percentageSum * 100, 2)

        scheduleListWeighted.append((episode, episodeInterest))

    return scheduleListWeighted

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
