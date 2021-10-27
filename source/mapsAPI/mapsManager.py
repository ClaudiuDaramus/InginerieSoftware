import urllib.parse
import requests


def getMapsUser(email='', password=''):
    parameters = {'user[email]': email, 'user[password]': password}
    parameters = urllib.parse.urlencode(parameters)
    link = 'https://uebermaps.com/api/v2/authentication?' + parameters
    print(link)

    response = requests.get(link)
    if response.status_code == 200:
        response = response.json()
        if response['meta']['code'] == 200:
            return {'result': response['data']}
        else:
            return {'error': response['meta']}
    else:
        return {'error': 'Server returned %s' % response.status_code}