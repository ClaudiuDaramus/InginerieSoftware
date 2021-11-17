from django.urls import path
from .views import Auth, IsAuthenticated, callback

urlpatterns = [
    path('get-auth-url', Auth.as_view()),
    path('redirect', callback),
    path('is-authenticated', IsAuthenticated.as_view())
]