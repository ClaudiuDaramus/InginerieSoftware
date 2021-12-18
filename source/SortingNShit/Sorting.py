import json

f = open("jsons.txt", "r")
watchHistory = json.load(f)

videoInterestKeys = [('rated', 0), ('director', 0), ('type', 0), ('genres', 1), ('actors', 1), ('languages', 1),
                     ('countries', 1), ('production', 1), ('writers', 1), ('runtime', 2), ('imdbRating', 3)]

percentageInterestKeys = [('rated', 0.2), ('director', 0.3), ('type', 0.1), ('genres', 0.3), ('actors', 0.5),
                          ('languages', 0.05), ('countries', 0.05), ('production', 0.3), ('writers', 0.5),
                          ('runtime', 0.1), ('imdbRating', 0.3)]


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
        'production': [elem.lower() for elem in response['Production'].split(',')] if response.get('Production') else [],
        'imdbRating': float(response['imdbRating'])
    }


def calculateVideoInterestScore(firstFilmList=None, secondFilmList=None, percentageSum = 2.7):
    if firstFilmList is None or secondFilmList is None:
        raise Exception('Method need both parameters')

    interestListScore = {}
    for firstFilm in firstFilmList:
        for secondFilm in secondFilmList:
            for (key, isSimple) in videoInterestKeys:
                if(firstFilm[key] == secondFilm[key] == "G" or firstFilm[key] == secondFilm[key] == "TV-Y" or
                        firstFilm[key] == secondFilm[key] == "TV-Y7"):
                    interestListScore[key] = 10.0
                elif isSimple == 0:
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
                elif isSimple == 3:
                    interestListScore[key] = 0

    interestValue = 0
    for key, score in percentageInterestKeys:
        if interestListScore[key] == 10.0:
            interestValue += 10.0
            percentageSum = 12.5
        else:
            interestValue += interestListScore[key] * score

    score = max(0,interestValue / percentageSum)

    return interestListScore, score


class MediaEntry:
    def __init__(self, media_details):
        self.rated = media_details["Rated"]
        self.runtime = int(media_details["Runtime"].split(' min')[0])
        self.genres = [elem.lower() for elem in media_details['Genre'].split(',')]
        self.director = media_details['Director']
        self.writers = [elem.lower() for elem in media_details['Writer'].split(',')]
        self.actors = [elem.lower() for elem in media_details['Actors'].split(',')]
        self.languages = [elem.lower() for elem in media_details['Language'].split(',')]
        self.countries = [elem.lower() for elem in media_details['Country'].split(',')]
        self.typeOfMedia = media_details['Type']
        self.production = [elem.lower() for elem in media_details['Production'].split(',')] if media_details.get('Production') else []
        self.imdbRating = float(media_details['imdbRating'])


watchedStuff = []

# print(type(watchHistory["movie_details"]))

for mediaType in watchHistory["movie_details"]:
    watchedStuff.append(MediaEntry(mediaType))

print(watchedStuff[0].imdbRating)
    # print([formatResponseForInterest(pair[1][0])])
    # for pair2 in pair[1][0].items():
    #     print(pair2[0])
    #print([formatResponseForInterest(pair[1][0])])
    # print(calculateVideoInterestScore([formatResponseForInterest(pair[1][0])], [formatResponseForInterest(pair[1][2])]))
