# from django.test import TestCase
# from rest_framework.authtoken.admin import User
#
# class WatchHistoryTests(TestCase):
#     def setUp(self):
#         self.client.force_login(User.objects.get_or_create(username='test')[0])
#
#     def test_findMovieView(self):
#         response = self.client.get('/watch-history/create/', data={"profileName": "test"})
#         self.assertEqual(response.status_code, 200)