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

from authentication.models import Profile
from authentication.serializers import UserSerializer, ProfileSerializer
from source.helpers import HelperFunctions, APIExtended
from .profileViews import createNewProfile


class UserRegisterView(APIExtended):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        fieldsString = HelperFunctions.getStringFromList(self.fieldsNormalized, ', ')
        self.parameters['description'] = 'This endpoint receives %s and creates an account' % fieldsString

    @staticmethod
    def createUser(data):

        if HelperFunctions.isEmptyDict(data):
            response = HelperFunctions.wrapResponse(info='no data was given')
            return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)

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

    def get(self, request):
        data = super().getRequestData(request)
        return self.createUser(data)

    def post(self, request):
        data = super().getRequestData(request)
        return self.createUser(data)


class UserLoginView(APIExtended):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # overwrite fields, normalization, description
        self.fieldsNormalized = ['username', 'password']
        self.fields = ['username', 'password']

        fieldsString = HelperFunctions.getStringFromList(self.fieldsNormalized, ', ')
        self.parameters['description'] = 'This endpoint receives %s and login into an account' % fieldsString

    @staticmethod
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

    def mainLogic(self, request):
        if request.user.id is not None:
            return Response(HelperFunctions.wrapResponse(info='user is already logged in'))
        else:
            data = super().getRequestData(request)
            return self.logInUser(data)

    def get(self, request):
        return self.mainLogic(request)

    def post(self, request):
        return self.mainLogic(request)

