from django.db import models

# Create your models here.

class Song(models.Model):
    shazam_key = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=120)
    artist = models.CharField(max_length=120)
    # cover = models.ImageField(upload_to='images')
    
    def __str__(self):
        return self.title
    
class ExternalLink(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    provider = models.CharField(max_length=120)
    uri = models.URLField()
    
    def __str__(self):
        return self.uri
class RedirectLink(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    provider = models.CharField(max_length=120)
    link = models.CharField(max_length=120)
    
    def __str__(self):
        return self.link