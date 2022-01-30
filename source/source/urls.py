"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, re_path
from django.contrib import admin
from rest_framework.authtoken import views
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(
    title='Server Monitoring API',
    url='https://www.example.org/api/',
)
# do not use mapsAPI, it is not useful or okay right now
urlpatterns = [
    # we make direct link between baseMaster app and site
    re_path(r'^main/', include('baseMaster.urls')),
    re_path(r'^movie/', include('movieAPI.urls')),
    re_path(r'^maps/', include('mapsAPI.urls')),
    re_path(r'^maps/', include('mapsAPI.urls')),
    re_path(r'^music/', include('musicAPI.urls')),
    re_path('api-token-auth/', views.obtain_auth_token),
    re_path(r'^auth/', include('authentication.urls')),
    re_path('swagger', schema_view)
]
