from __future__ import absolute_import, unicode_literals

from source.celery import app

import logging
import base64
import http.client
import json
import sys
import asyncio
from argparse import ArgumentParser
from urllib.error import HTTPError
import ffmpeg
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from source.celery import app

@app.task(name="song_task")
def song_task(url):
    try:
        conn = http.client.HTTPSConnection("shazam.p.rapidapi.com")

        payload = asyncio.run(get_payload(url)).decode()
        headers = {
            'content-type': "text/plain",
            'x-rapidapi-host': "shazam.p.rapidapi.com",
            'x-rapidapi-key': "609ebb9d7cmsh62ae3675c254ed3p11269bjsn7fe8ea3d562f"
            }

        conn.request("POST", "/songs/detect", payload, headers)

        res = conn.getresponse()
    except HTTPError as err:
        print("[err:] Couldn't find song")
        
    data = res.read().decode()

async def get_payload(url):
    process1 = await asyncio.create_subprocess_shell(f'youtube-dl -g {url}', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stream, err = await process1.communicate()

    print(f'[exited with {process1.returncode}]')
    if stream:
        print(stream.decode())
    if err:
        print(f'[err:]\n{err.decode()}')
        sys.exit(1)

    try:
        process2 = ffmpeg.input(stream.decode()).output('pipe:',ss=0, t=4, ac=1,format='s16le', acodec='pcm_s16le', ar=44100).run_async(pipe_stdout=True)
        with process2.stdout as buffer:
            bytes = base64.b64encode(buffer.read())
            buffer.close()
            return bytes
    except ffmpeg.Error as err:
        print(f"[err:] FFmpeg failed {err}")
        sys.exit(1)

# def translate_request(data):
#     data = json.loads(data)

#     song = dict()
#     song['key'] = data['matches'][0]['id']
    
#     data = data['track']
    
#     song['title'] = data['title']
#     song['artist'] = data['subtitle']
#     song['cover'] = data['images']['background']
    
#     song['search_links'] = dict()
#     song['search_links']['spotify'] = data['hub']['providers'][0]['actions'][0]['uri']
#     song['search_links']['deezer'] = data['hub']['providers'][1]['actions'][0]['uri']
    
#     song['external_links'] = dict()
#     song['external_links']['shazam'] = data['url']
#     song['external_links']['apple'] = data['hub']['options'][0]['actions'][1]['uri']
#     song['external_links']['itunes'] = data['hub']['options'][1]['actions'][0]['uri']
    
#     return song
    
# def print_song(song):    
#     print(f"\n\nTitle: {song['title']} \nArtist: {song['artist']} \nCover: {song['cover']}")
#     print(f"\n\nExternal links:\nShazam: {song['external_links']['shazam']} \nApple Music: {song['external_links']['apple']}\niTunes: {song['external_links']['itunes']}")
#     print(f"\n\nSearch:\nSpotify: {song['search_links']['spotify']}\nDeezer: {song['search_links']['deezer']}")
    
# def parse_args(args):
#     parser = ArgumentParser(description='Identify currently playing song.')
#     parser.add_argument('url', type=str, help="livestream url")
#     parser.add_argument('--recommendations', type=bool, default=False, help='recommend similar songs')
#     url = vars(parser.parse_args(sys.argv[1:]))['url']
# if __name__ == '__main__':
#     parser = ArgumentParser(description='Identify currently playing song.')
#     parser.add_argument('url', type=str, help="livestream url")
#     parser.add_argument('--recommendations', type=bool, default=False, help='recommend similar songs')
#     url = vars(parser.parse_args(sys.argv[1:]))['url']
#     validate = URLValidator()
#     try:
#         validate(url)
#     except ValidationError as exception:
#         logger(f"[err:] ${url} is not a valid URL")
#         sys.exit(1)

#     try:
    
#         conn = http.client.HTTPSConnection("shazam.p.rapidapi.com")

#         payload = asyncio.run(get_payload(url)).decode()
#         headers = {
#             'content-type': "text/plain",
#             'x-rapidapi-host': "shazam.p.rapidapi.com",
#             'x-rapidapi-key': "609ebb9d7cmsh62ae3675c254ed3p11269bjsn7fe8ea3d562f"
#             }

#         conn.request("POST", "/songs/detect", payload, headers)

#         res = conn.getresponse()
#     except HTTPError as err:
#         print("[err:] Couldn't find song")
        
#     data = res.read().decode()
#     song = translate_request(data)
#     try:
    
#         conn = http.client.HTTPConnection("http://127.0.0.1/music/post", 8000)

#         payload = json.dumps(song)
#         headers = {
#             'content-type': "application/json",
#             }

#         conn.request("POST", "/songs/detect", payload, headers)

#         res = conn.getresponse()
#     except HTTPError as err:
#         print("[err:] Couldn't send song")
    

