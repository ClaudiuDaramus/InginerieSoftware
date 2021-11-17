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

from .serializers import UserSerializer, ProfileSerializer
from .models import Profile
from source.helpers import HelperFunctions, APIExtended
from rest_framework.generics import GenericAPIView


def createNewProfile(data, user):
    # if data is {}:
    # return Response(HelperFunctions.wrapResponse(info='bad'))
    if HelperFunctions.isEmptyDict(data):
        return Response(HelperFunctions.wrapResponse(info='This call has no data'), status=status.HTTP_406_NOT_ACCEPTABLE)

    # return JsonResponse({'value': profileSerializer.is_valid()})
    randomString = str(uuid4())[0:19]
    profileName = data.get('profileName') if data.get('profileName') else randomString

    found = Profile.objects.filter(profileName=profileName).first()
    if found is not None:
        # profileName = randomString
        return Response({'error': 'a profile with this name already exists'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    profileSerializer = ProfileSerializer(data={'profileName': profileName})
    if profileSerializer.is_valid():
        newProfileDict = {
            'profileName': profileSerializer.validated_data['profileName'],
            'user': user,
        }
        try:
            profile = profileSerializer.create(validated_data=newProfileDict)
            return Response({'profile': ProfileSerializer.getJsonVariant(profile), 'error': None},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': e.args}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': profileSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)