from django.db import models


# Create your models here.
class movieHistory(models.Model):
    title = models.CharField(max_length=120)
    genre = models.CharField(max_length=120)
    rated = models.IntegerField(blank=False, null=False)
    director = models.CharField(max_length=120)
    type = models.CharField(max_length=120)
    actors = models.CharField(max_length=120)
    languages = models.CharField(max_length=120)
    countries = models.CharField(max_length=120)
    production = models.CharField(max_length=120)
    writers = models.CharField(max_length=120)
    runtime = models.CharField(max_length=120)

    def __str__(self):
        return self.title
