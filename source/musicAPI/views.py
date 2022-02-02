from rest_framework import status, request
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tasks import song_task
import base64
import ffmpeg
import json
import unittest
# # Create your views here.
# @api_view(['POST'])
# def save_song(request):
#     serializer = SongSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

test = unittest.TestCase()

@api_view(['GET'])
def get_playing_song(req):
    if req.GET.get('url', None) is not None:
        song_task(req.GET.get('url'))
    test.fail('url not set')
    