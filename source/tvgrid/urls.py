from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.authtoken import views
from .views import updateTVSchedule

urlpatterns = [
    url('update/', updateTVSchedule, name='search'),
]
