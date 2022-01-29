from django.db import models


# Create your models here.
class MediaEntry(models.Model):
    channel = models.CharField(max_length=50, default='')
    program = models.CharField(max_length=50, default='')
    description = models.CharField(max_length=1000, default='')
    starting_time = models.TimeField(auto_now_add=True)
    duration = models.IntegerField(default=0)  # number of minutes
    type = models.CharField(max_length=50, default='')
