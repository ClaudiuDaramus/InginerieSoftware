from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
import json
import os

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

from .serializers import UserSerializer

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
        return JsonResponse(serializedUser.errors)

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
