"""source URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework.authtoken import views
from django.contrib import admin
from django.urls import re_path, include

urlpatterns = [
    re_path(r'^auth/', include('authentication.urls')),
    re_path('api-token-auth/', views.obtain_auth_token),
    re_path(r'^main/', include('baseMaster.urls')),
    re_path(r'^movie/', include('movieAPI.urls')),
    re_path(r'^maps/', include('mapsAPI.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^music/', include('musicAPI.urls'))
    # url(r'^grid/', include('GridRecommendation.urls')),
]
