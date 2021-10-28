import rest_framework.decorators
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
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.decorators import renderer_classes
from rest_framework import generics
from rest_framework import mixins
from rest_framework.settings import api_settings

from rest_framework import status

from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from authentication.serializers import UserSerializer, ProfileSerializer
from authentication.models import Profile
from source.helpers import optionHelper, getStringFromList, APIExtended

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createNewProfile(request):
    # return JsonResponse({'value': profileSerializer.is_valid()})
    randomString = str(uuid4())[0:19]
    profileName = request.data.get('profileName') if request.data.get('profileName') else randomString

    found = Profile.objects.filter(profileName=profileName).first()
    if found is not None:
        # profileName = randomString
        return Response({'error': 'a profile with this name already exists'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    profileSerializer = ProfileSerializer(data={'profileName': profileName})
    if profileSerializer.is_valid():
        newProfileDict = {
            'profileName': profileSerializer.validated_data['profileName'],
            'user': request.user,
        }
        try:
            profile = profileSerializer.create(validated_data=newProfileDict)
            return Response({'profile': ProfileSerializer.getJsonVariant(profile), 'error': None}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': e.args}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': profileSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfiles(request, name=None):
    newProfileList = []
    profiles = Profile.objects.filter(user=request.user)

    if name is not None:
        profile = profiles.filter(profileName=name).first()
        if profile is None:
            response = {'error': 'There is no profile with this name'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        response = ProfileSerializer.getJsonVariant(profile)
        return Response({'results': response, 'error': None}, status=status.HTTP_200_OK)
    else:
        profiles = [ProfileSerializer.getJsonVariant(profile) for profile in profiles]
        response = {'results': newProfileList, 'number of profiles': len(profiles), 'error': None}
        return Response(response, status.HTTP_200_OK)


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
