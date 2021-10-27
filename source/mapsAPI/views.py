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

from authentication.models import Profile
from authentication.serializers import ProfileSerializer, UserSerializer

from .mapsManager import getMapsUser

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMapsAuth(request):
    email = request.GET.get('email')
    password = request.GET.get('password')

    if email is None or password is None:
        return JsonResponse({'error': 'This endpoint needs two parameters'})
    else:
        response = getMapsUser(email, password)
        return JsonResponse(response)