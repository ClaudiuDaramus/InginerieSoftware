import asyncio
import http
from urllib import response
from django.test import Client
import base64
import unittest
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import ffmpeg
# Create your tests here.
class AsyncioTest(unittest.IsolatedAsyncioTestCase):
    badURL = ".youtube.com/watch?"
    goodURL = "https://www.youtube.com/watch?v=5vgw9F5CZRQ"
    async def test_get_stream(self):
        result = await asyncio.create_subprocess_shell(f'youtube-dl -g {self.goodURL}', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE) 
        stream, err = await result.communicate()
        self.assertFalse(bool(err))
        return stream.decode()

    async def test_get_stream_invalid(self):
        result = await asyncio.create_subprocess_shell(f'youtube-dl -g {self.badURL}', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE) 
        stream, err = await result.communicate()
        self.assertTrue(bool(err))
        return stream

class StreamTest(unittest.TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.invalidURL = "radfasd"
        self.wrongURL = "https://www.youtube.com/watch?v=HEehzNXtDY0"
        self.goodURL = "https://www.youtube.com/watch?v=5vgw9F5CZRQ"

    def test_url_parsing_fails(self):
        validator = URLValidator()
        with self.assertRaises(ValidationError) as err:
            validator(self.invalidURL)
        try:
            URLValidator(self.wrongURL)
            URLValidator(self.goodURL)
        except ValidationError:
            self.fail("url raised ValidationError unexpectedly!")

    def test_valid_stream(self):
        self.validStream = asyncio.run(AsyncioTest('test_get_stream').test_get_stream())
        self.assertEquals(self.validStream[-5:], "m3u8\n")
        
    def test_invalid_stream(self):
        self.invalidStream = asyncio.run(AsyncioTest('test_get_stream_invalid').test_get_stream_invalid())
        self.assertNotEqual(self.invalidStream[-5:], "m3u8\n")


    # TODO: change this
    # def test_ffmpeg_invalid(self):
    #     try:
    #         process = ffmpeg.input(self.validStream.decode()).output('pipe:',ss=0, t=4, ac=1,format='s16le', acodec='pcm_s16le', ar=44100).run_async(pipe_stdout=True)
    #         with process.stdout as buffer:
    #             bytes = base64.b64encode(buffer.read())
    #             buffer.close()
    #             return bytes
    #     except ffmpeg.Error as err:
    #         self.fail(f'FFmpeg failed with {err}!')
            
    # def test_ffmpeg_valid(self):
    #     with self.assertRaises(Error):
    #         process = ffmpeg.input(self.validStream.decode()).output('pipe:',ss=0, t=4, ac=1,format='s16le', acodec='pcm_s16le', ar=44100).run_async(pipe_stdout=True)
    #         with process.stdout as buffer:
    #             self.payload = base64.b64encode(buffer.read())
    #             buffer.close()
    

