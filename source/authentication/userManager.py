import requests
import urllib.parse

link = 'https://randomuser.me/api/?'

parametersDict = {
    'gender': ('male', 'female', None),
    'results': (1, 5000),
}


# https://randomuser.me/api/?password=special,upper,lower,number
# https://randomuser.me/api/?seed=foobar

def getPersonList(listSize=10, gender=None):
    minSize, maxSize = parametersDict['results']
    # return {'min': minSize, 'max': maxSize, 'size': listSize}
    if listSize > maxSize or listSize < minSize:
        raise Exception('The list size cannot be greater than 5000 or less than 1')

    if gender not in parametersDict['gender']:
        raise Exception('This is not valid gender')

    parameters = {'results': listSize}
    if gender is not None:
        parameters['gender'] = gender

    response = requests.get(link + urllib.parse.urlencode(parameters))

    if response.status_code != 200:
        raise Exception('The serve raised error %s' % response.status_code)

    response = response.json()
    response = response['results'], response['info']['seed']

    return response


def getPersonBySeed(seed='random'):
    response = requests.get(link + urllib.parse.urlencode({'seed': seed}))
    return response.json()


#            'password': instance.password
def filterPersons(personList):
    try:
        newPersonList = []
        for person in personList:
            location = person['location']
            newPersonList.append({
                'gender': person['gender'],
                'first name': person['name']['first'],
                'last name': person['name']['last'],
                'title': person['name']['title'],
                'street': location['street']['name'] + str(location['street']['number']),
                'city': location['city'],
                'state': location['state'],
                'country': location['country'],
                'email': person['email'],
                'username': person['login']['username'],
                'password': person['login']['password'],
                'phone': person['phone'],
                'picture small': person['picture']['thumbnail'],
                'picture medium': person['picture']['medium'],
                'picture large': person['picture']['large'],
                'nationality': person['nat']
            })

        return newPersonList
    except Exception as e:
        raise Exception(e.args)
