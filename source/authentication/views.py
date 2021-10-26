from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
import json
import os
from uuid import uuid4

import requests
from django.contrib.auth import authenticate

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token

from django.shortcuts import render, get_object_or_404, get_list_or_404

from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins

from rest_framework import status

from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django.contrib.auth.models import User

from .serializers import UserSerializer, ProfileSerializer
from .models import Profile
from .userManager import getPersonList, filterPersons

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializedUser = UserSerializer(data=request.data)
    if serializedUser.is_valid():
        print(serializedUser.validated_data)
        user = serializedUser.create(validated_data=serializedUser.validated_data)
        token, created = Token.objects.get_or_create(user=user)

        response = JsonResponse({'user': serializedUser.getJsonVariant(user), 'token': token.key})
        response.set_cookie('auth_token', token.key)

        return response
    else:
        return JsonResponse({'error': serializedUser.errors})

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):

    user = User.objects.filter(username=request.data['username']).first()
    token, created = Token.objects.get_or_create(user=user)
    response = JsonResponse({'user': UserSerializer.getJsonVariant(user), 'token': token.key})
    response.set_cookie('auth_token', token.key)
    return response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dummyView(request):
    return JsonResponse({'good': 'u see this'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createNewProfile(request):
    # return JsonResponse({'value': profileSerializer.is_valid()})
    randomString = str(uuid4())[0:19]
    profileName = request.data.get('profileName') if request.data.get('profileName') else randomString

    found = Profile.objects.filter(profileName=profileName).first()
    if found is not None:
        # profileName = randomString
        return JsonResponse({'error': 'a profile with this name already exists'})

    profileSerializer = ProfileSerializer(data={'profileName': profileName})
    if profileSerializer.is_valid():
        newProfileDict = {
            'profileName': profileSerializer.validated_data['profileName'],
            'user': request.user,
        }
        try:
            profile = profileSerializer.create(validated_data=newProfileDict)
            return JsonResponse({'profile': ProfileSerializer.getJsonVariant(profile), 'error': None})
        except Exception as e:
            return JsonResponse({'error': e.args})
    else:
        return JsonResponse({'error': profileSerializer.errors})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllProfiles(request):
    newProfileList = []
    profiles = Profile.objects.filter(user=request.user)
    for profile in profiles:
        newProfileList.append(ProfileSerializer.getJsonVariant(profile))
    return JsonResponse({'results': newProfileList, 'number of profiles': len(profiles), 'error': None})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def updateProfile(request):
    newProfileName = request.GET.get('newProfileName')
    profileName = request.GET.get('profileName')
    if profileName is None or profileName == '':
        return JsonResponse({'error': 'A profile name is needed to make the changed'})

    if newProfileName is None or newProfileName == '':
        return JsonResponse({'error': 'A new profile name is needed to make the change'})

    profile = Profile.objects.filter(profileName=profileName).first()
    if profile is None:
        return JsonResponse({'error': 'A profile with this name was not found'})

    serializedProfile = ProfileSerializer(data={'profileName': newProfileName})
    if serializedProfile.is_valid():
        try:
            updatedProfile = serializedProfile.update(profile, serializedProfile.validated_data)
            return JsonResponse({'result': ProfileSerializer.getJsonVariant(updatedProfile), 'error': None})
        except Exception as e:
            return JsonResponse({'error': e.args})
    else:
        return JsonResponse({'error': serializedProfile.errors})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deleteProfile(request):
    profileName = request.GET.get('profileName')

    if profileName is None or profileName == '':
        return JsonResponse({'error': 'A profile name is needed to make the delete'})

    profile = Profile.objects.filter(profileName=profileName).first()
    if profile is None:
        return JsonResponse({'error': 'A profile with this name was not found'})

    profileJson = ProfileSerializer.getJsonVariant(profile)
    profile.delete()

    return JsonResponse({'result': profileJson, 'error': None})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getFakeList(request):
    listSize = request.GET.get('listSize')
    gender = request.GET.get('gender')

    # we can populate the database with some users
    try:
        if listSize is None:
            response, seed = getPersonList(gender=gender)
        else:
            response, seed = getPersonList(int(listSize), gender=gender)

        response = filterPersons(response)
        return JsonResponse({'results': response, 'seed': seed, 'error': None})
    except Exception as e:
        return JsonResponse({'error': e})
