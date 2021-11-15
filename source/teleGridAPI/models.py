from django.db import models


# Create your models here.
class Language(models.Model):
    name = models.CharField(max_length=50)


class Category(models.Model):
    name = models.CharField(max_length=50)


class Channel(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class TimeSlot(models.Model):
    name = models.CharField(max_length=50)
    details = models.CharField(max_length=1000)
    type = models.CharField(max_length=50)
    startTime = models.DateTimeField()
