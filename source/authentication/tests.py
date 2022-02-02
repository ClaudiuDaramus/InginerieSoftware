from django.test import TestCase
from rest_framework.authtoken.admin import User

from .models import Profile


class AuthenthicationTests(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.get_or_create({
            "username": "test",
            "email": "test@test.com",
            "last_name": "test",
            "first_name": "test",
            "password": "tesT1234!"
        })

    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='test')[0])

    def test_register(self):
        response = self.client.post('/auth/register/', data =
        {
            "username": "test5",
            "email": "test5@test.com",
            "last name": "test5",
            "first name": "test5",
            "password": "tesT1234!"
        })
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        response = self.client.get('/auth/login/', data ={"username": "test"})
        self.assertEqual(response.status_code, 200)

    def test_createNewProfile(self):
        response = self.client.post('/auth/create/profile/', data={"profileName" : "test"})
        self.assertEqual(response.status_code, 201)

    def test_getProfiles(self):
        response = self.client.get('/auth/get/profiles/')
        self.assertEqual(response.status_code, 200)

    def test_updateProfile(self):
        response = self.client.get('/auth/update/profile/', data={"profileName" : "test", "newProfileName" : "test5"})
        self.assertEqual(response.status_code, 200)

    def test_deleteProfile(self):
        response = self.client.get('/auth/delete/profile/', data={"profileName" : "test"})
        self.assertEqual(response.status_code, 200)