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
from django.contrib.auth.models import User

# from .serializers import
from authentication.serializers import UserSerializer, ProfileSerializer
from authentication.userManager import getPersonList, filterPersons

from source.helpers import HelperFunctions, APIExtended

# TODO make some endpoint as GET for simple testing
# TODO use renderer_classes to use rendered response by drf
# TODO create a swagger by using drf renderer and making an automation for endpointsDescription


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dummyView(request):
    data = {'good': 'u see this', 'user': UserSerializer.getJsonVariant(request.user)}
    return Response(data, status=status.HTTP_200_OK)


# class ProfileView(APIExtended):
#     permission_classes = [AllowAny]
#
#     def __init__(self, **kwargs):
#         super().__init__(ProfileSerializer, **kwargs)
#
#     def options(self, request, *args, **kwargs):
#
#         fieldsString = getStringFromList(self.fieldsNormalized, ', ')
#
#         self.parameters = optionHelper(request, self, {
#             'description': 'This endpoints receives %s and creates an account' % fieldsString,
#         })
#         return super().options(request, args, kwargs)
#
#     def get(self, request):
#         data = super().getTransform(request)
#         return self.createUser(data)
#
#     def post(self, request):
#         data = super().postTransform(request)
#         return self.createUser(data)


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

        # create fake users and add to db
        for person in response:
            serializedUser = UserSerializer(data=person)
            if serializedUser.is_valid():
                try:
                    user = serializedUser.create(validated_data=serializedUser.validated_data)
                except Exception as e:
                    return JsonResponse({'error': e.args})
            else:
                return JsonResponse({'error': serializedUser.errors})

        return JsonResponse({'result': response, 'seed': seed, 'error': None})
    except Exception as e:
        return JsonResponse({'error': e})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserLocation(request):
    ip = request.GET.get('ip')
    response = requests.get('http://ipwhois.app/json/%s' % ip)

    if response.status_code == 200:
        response = response.json()
        if response['success'] is False:
            return JsonResponse({'error': response['message']})
        else:
            return JsonResponse({'result': response})
    else:
        return JsonResponse({'error': 'The server returned %s' % response.status_code})
