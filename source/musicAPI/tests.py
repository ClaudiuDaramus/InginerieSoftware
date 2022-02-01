from urllib import response
from django.test import TestCase, Client
from .views import get_playing_song
import unittest
# Create your tests here.

class TestGetSong(unittest.TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.invalidURL = self.client.get("radfasd")
        self.wrongURL = self.client.get("https://www.youtube.com/watch?v=HEehzNXtDY0")
        self.goodURL = self.client.get("https://www.youtube.com/watch?v=5vgw9F5CZRQ")
        return super().setUp()

c = Client()