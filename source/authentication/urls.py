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
from django.conf.urls import url
from rest_framework.authtoken import views
from .views import register, dummyView, login, createNewProfile, getAllProfiles, updateProfile, deleteProfile, \
    getFakeList, getUserLocation, UserRegisterView

urlpatterns = [
    url('api-token-auth/', views.obtain_auth_token, name='auth'),
    url('view/register/', UserRegisterView.as_view(), name='register-view'),
    url('register/', register, name='register'),
    url('dummy/', dummyView, name='dummy'),
    url('login/', login, name='login'),
    url('create/profile/', createNewProfile, name='create-profile'),
    url('get/profiles/', getAllProfiles, name='get-profiles'),
    url('update/profile/', updateProfile, name='update-profile'),
    url('delete/profile/', deleteProfile, name='delete-profile'),
    url('get/fakes/', getFakeList, name='get-fake-persons'),
    url('location/', getUserLocation, name='get-location'),
]
