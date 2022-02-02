from django.test import TestCase
from rest_framework.authtoken.admin import User
from django.contrib.auth.models import User

class TVGridTests(TestCase):

    def setUp(self):
        self.client.force_login(User.objects.create_superuser("test", "test@test.com", "test"))

    def test_viewSchedule(self):
        response = self.client.get('/tv/schedule/')
        self.assertEqual(response.status_code, 200)

    def test_updateTVSchedule(self):
        response = self.client.get('/tv/update/')
        self.assertEqual(response.status_code, 200)

    def test_functionTesting(self):
        response = self.client.get('/tv/test/')
        self.assertEqual(response.status_code, 200)