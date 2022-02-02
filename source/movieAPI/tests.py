from django.test import TestCase
from rest_framework.authtoken.admin import User
from .movieManager import searchForVideoContent, calculateVideoInterestScoreUpgraded, formatResponseForInterest


class MovieAPITests(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='test')[0])

    def test_searchForMovieView(self):
        response = self.client.get('/movie/search/', data={"title": "alchemist"})
        self.assertEqual(response.status_code, 200)


    def test_findMovieView(self):
        response = self.client.get('/movie/find/', data={"title": 'avatar'})
        self.assertEqual(response.status_code, 200)

    # NOT READY
    # def test_calculateVideoInterestScore(self):
    #     firstUserSearch = searchForVideoContent(title='avatar')
    #     secondUserSearch = searchForVideoContent(title='the last airbender')
    #     firstSearchFormatted = formatResponseForInterest(firstUserSearch)
    #     secondSearchFormatted = formatResponseForInterest(secondUserSearch)
    #     score = calculateVideoInterestScoreUpgraded([firstSearchFormatted], [secondSearchFormatted])
    #     self.assertTrue(score)