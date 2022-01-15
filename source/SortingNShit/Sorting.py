import json

from Resources.HelperClasses import MediaEntry

f = open("Resources/Jsons/dummyMovieHistory.txt", "r")
watchHistory = json.load(f)

videoInterestKeys = [('rated', 0), ('director', 0), ('type', 0), ('genres', 1), ('actors', 1), ('languages', 1),
                     ('countries', 1), ('production', 1), ('writers', 1), ('runtime', 2), ('imdbRating', 3)]

percentageInterestKeys = [('rated', 0.2), ('director', 0.3), ('type', 0.1), ('genres', 0.3), ('actors', 0.5),
                          ('languages', 0.05), ('countries', 0.05), ('production', 0.3), ('writers', 0.5),
                          ('runtime', 0.1), ('imdbRating', 0.3)]


def calculate_video_interest_score(first_film_list=None, second_film_list=None, percentage_sum=2.7):
    if first_film_list is None or second_film_list is None:
        raise Exception('Method need both parameters')

    interest_list_score = {}
    for first_film in first_film_list:
        for second_film in second_film_list:
            for (key, isSimple) in videoInterestKeys:
                if (first_film[key] == second_film[key] == "G" or first_film[key] == second_film[key] == "TV-Y" or
                        first_film[key] == second_film[key] == "TV-Y7"):
                    interest_list_score[key] = 10.0
                elif isSimple == 0:
                    if first_film[key] == second_film[key]:
                        interest_list_score[key] = 1
                    else:
                        interest_list_score[key] = 0
                elif isSimple == 1:
                    counter = 0
                    for firstElem in first_film[key]:
                        if firstElem in second_film[key]:
                            counter += 1
                    interest_list_score[key] = 1.0 * counter / max(len(first_film[key]), len(second_film[key]))
                elif isSimple == 2:
                    min_length = min(first_film[key], second_film[key]) * 1.0
                    max_length = max(first_film[key], second_film[key]) * 1.0

                    interest_list_score[key] = min_length / max_length
                elif isSimple == 3:
                    interest_list_score[key] = 0

    interest_value = 0
    for key, score in percentageInterestKeys:
        if interest_list_score[key] == 10.0:
            interest_value += 10.0
            percentage_sum = 12.5
        else:
            interest_value += interest_list_score[key] * score

    score = max(0, interest_value / percentage_sum)

    return interest_list_score, score


watchedStuff = []

# print(type(watchHistory["movies"]))

for mediaType in watchHistory["movies"]:
    watchedStuff.append(MediaEntry.MediaEntry(mediaType))

print(watchedStuff[0].imdbRating)
# print([formatResponseForInterest(pair[1][0])])
# for pair2 in pair[1][0].items():
#     print(pair2[0])
# print([formatResponseForInterest(pair[1][0])])
# print(calculateVideoInterestScore([formatResponseForInterest(pair[1][0])], [formatResponseForInterest(pair[1][2])]))
