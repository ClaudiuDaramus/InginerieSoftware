from django.test import TestCase
from rest_framework.authtoken.admin import User
from .movieManager import searchForVideoContent, calculateVideoInterestScoreUpgraded, oldFormatResponseForInterest


class MovieAPITests(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='test')[0])

    def test_searchForMovieView(self):
        response = self.client.get('/movie/search/', data={"title": "alchemist"})
        self.assertEqual(response.status_code, 200)

    # def test_findMovieView(self):
    #     response = self.client.get('/movie/find/', data={"title": 'avatar', "imdbID": 'tt0499549'})
    #     self.assertEqual(response.status_code, 200)

    def test_compareMovieListView(self):
        firstUserSearch = searchForVideoContent(title='avatar')
        secondUserSearch = searchForVideoContent(title='the last airbender')
        response = self.client.get('/movie/compare/list/', data={"firstList" :[firstUserSearch], "firstIdList":[firstUserSearch["imdbID"]], "secondList":[secondUserSearch], "secondIdList":[secondUserSearch["imdbID"]]})
        self.assertEqual(response.status_code, 200)

    def test_compareMoviesView(self):
        firstUserSearch = searchForVideoContent(title='avatar')
        secondUserSearch = searchForVideoContent(title='the last airbender')
        response = self.client.get('/movie/compare/', data={"firstTitle" : "avatar", "firstImdbId":firstUserSearch["imdbID"], "secondTitle":'the last airbender', "secondImdbId":secondUserSearch["imdbID"]})
        self.assertEqual(response.status_code, 200)

    # def test_createContent(self):
    #     response = self.client.get('/movie/create')
    #     self.assertEqual(response.status_code, 200)

    # def test_calculateVideoInterestScore(self):
    #     # firstUserSearch = searchForVideoContent(title='avatar')
    #     # secondUserSearch = searchForVideoContent(title='the last airbender')
    #     # firstSearchFormatted = oldFormatResponseForInterest(firstUserSearch)
    #     # secondSearchFormatted = oldFormatResponseForInterest(secondUserSearch)
    #     # score = calculateVideoInterestScoreUpgraded([firstSearchFormatted], [secondSearchFormatted])
    #
    #     score = calculateVideoInterestScoreUpgraded(None, None)
    #     self.assertTrue(score)