from django.db import models


class Genre(models.Model):
    genre = models.CharField(max_length=20)


class Writer(models.Model):
    name = models.CharField(max_length=50)


class Actor(models.Model):
    name = models.CharField(max_length=50)


# Create your models here.
class VideoContent(models.Model):
    title = models.CharField(max_length=100)
    year = models.CharField(max_length=20)
    rated = models.CharField(max_length=10)
    released = models.DateField()  # '%Y-%m-%d
    runtime = models.IntegerField(null=True)
    genres = models.ManyToManyField(Genre)
    director = models.CharField(max_length=20, null=True)
    writers = models.ManyToManyField(Writer)
    actors = models.ManyToManyField(Actor)
    plot = models.CharField(max_length=1500)
