from musicAPI.serializers import SongSerializer
from rest_framework import status, request
from rest_framework.decorators import api_view
from rest_framework.response import Response
from musicAPI.tasks import get
import base64
import ffmpeg

# Create your views here.
@api_view(['POST'])
def save_song(request):
    serializer = SongSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_playing_song(res: Response):
    stream = res.getvalue('stream').decode()
    
    