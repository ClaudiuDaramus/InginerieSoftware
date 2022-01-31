from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.authtoken import views
from .views import updateTVSchedule, functionTesting, viewSchedule

urlpatterns = [
    url('update/', updateTVSchedule, name='search'),
    url('test/', functionTesting, name='test'),
    url('schedule/', viewSchedule, name='schedule'),
]
