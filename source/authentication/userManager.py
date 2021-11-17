import requests
import urllib.parse
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.settings import api_settings

from rest_framework import status

from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django.contrib.auth.models import User

from .models import Profile
from .serializers import UserSerializer, ProfileSerializer
from source.helpers import HelperFunctions, APIExtended

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


def filterPersons(personList):
    try:
        newPersonList = []
        for person in personList:
            location = person['location']
            newPersonList.append({
                'gender': person['gender'],
                'first_name': person['name']['first'],
                'last_name': person['name']['last'],
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


def createUser(data):
    if HelperFunctions.isEmptyDict(data):
        response = HelperFunctions.wrapResponse(info='no data was given')
        return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        serializedUser = UserSerializer(data=data)
        if serializedUser.is_valid():
            user = serializedUser.create(validated_data=serializedUser.validated_data)
            token, created = Token.objects.get_or_create(user=user)

            response = HelperFunctions.wrapResponse(results={
                'user': serializedUser.getJsonVariant(user),
                'token': token.key})

            response = Response(response, status=status.HTTP_201_CREATED)
            response.set_cookie('auth_token', token.key)

            return response
        else:
            response = HelperFunctions.wrapResponse(errors=serializedUser.errors)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


def logInUser(data):
    # TODO password verification

    if HelperFunctions.isEmptyDict(data):
        response = HelperFunctions.wrapResponse(info='no data was given')
        return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)

    user = User.objects.filter(username=data['username']).first()
    if user is None:
        response = HelperFunctions.wrapResponse(errors='User not found')
        response = Response(response, status=status.HTTP_404_NOT_FOUND)
    else:
        token, created = Token.objects.get_or_create(user=user)

        response = HelperFunctions.wrapResponse(results={'user': UserSerializer.getJsonVariant(user),
                                                         'token': token.key})

        response = Response(response, status=status.HTTP_200_OK)
        response.set_cookie('auth_token', token.key)

    return response