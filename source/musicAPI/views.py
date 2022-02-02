from django.shortcuts import redirect
import environ
import requests
from requests.api import post
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .util import is_spotify_authenticated, update_or_create_user_tokens

env = environ.Env()
environ.Env.read_env('.env')

class Auth(APIView):
    def get(self, request, format=None):
        scopes='playlist-modify-private playlist-read-private playlist-modify-public playlist-read-collaborative'
        url = requests.Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': env['REDIRECT_URI'],
            'client_id': env['CLIENT_ID']
        }).prepare().url

        return Response({'url': url}, status=status.HTTP_200_OK)

def callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': env['REDIRECT_URI'],
        'client_id': env['CLIENT_ID'],
        'client_secret': env['CLIENT_SECRET']
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_or_create_user_tokens(request.session.session_key, access_token, token_type, expires_in, refresh_token)
    return redirect('')

class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(self.request.session.session_key)
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)