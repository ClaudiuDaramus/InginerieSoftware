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

class SpotifyToken(models.Model):
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.CharField(max_length=150)
    access_token = models.CharField(max_length=150)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)