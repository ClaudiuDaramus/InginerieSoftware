from django.test import TestCase
from rest_framework.authtoken.admin import User

class WatchHistoryTests(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='test')[0])
        self.client.post('/auth/create/profile/', data={"profileName" : "test"})

    def test_findMovieView(self):
        response = self.client.get('/history/create/', data={"profileName" : "test", "isLiked" : "True"})
        self.assertEqual(response.status_code, 200)

    def test_createAutomatedHistory(self):
        response = self.client.get('/history/create/automated/')
        self.assertEqual(response.status_code, 200)