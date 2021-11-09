from django.db import models

# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=50)
    spotify_url = models.URLField(max_length=200)
class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    spotify_url = models.URLField(max_length=200)
    
class Song(models.Model):
    name = models.CharField(max_length=100)
    spotify_url = models.URLField(max_length=200)
    artists = models.ManyToManyField(Artist)
    genres = models.IntegerField()