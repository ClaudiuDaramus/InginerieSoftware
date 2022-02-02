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
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.authtoken import views

# do not use mapsAPI, it is not useful or okay right now
urlpatterns = [
    # we make direct link between baseMaster app and site
    url(r'^main/', include('baseMaster.urls')),
    url(r'^movie/', include('movieAPI.urls')),
    url(r'^maps/', include('mapsAPI.urls')),
    url(r'^music/', include('musicAPI.urls')),
    url(r'^admin/', admin.site.urls),
    url('api-token-auth/', views.obtain_auth_token),
    url(r'^auth/', include('authentication.urls')),
    url(r'^grid/', include('GridRecommendation.urls')),
    url(r'^tv/', include('tvgrid.urls')),
    url(r'^history/', include('watchHistory.urls')),

]