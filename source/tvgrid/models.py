from django.db import models
from .helpers import getManyOrNone, getTimeString
from authentication.models import Profile


class Genre(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Day(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Channel(models.Model):
    externalId = models.IntegerField()
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50, null=True)
    countryCode = models.CharField(max_length=5, null=True)
    type = models.CharField(max_length=5)

    def getJSONVariant(self):
        return {
            'externalId': self.externalId,
            'name': self.name,
            'country': self.country,
            'countryCode': self.countryCode,
            'type': self.type
        }


class Show(models.Model):
    externalId = models.IntegerField()
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=20, null=True)
    genres = models.ManyToManyField(Genre)
    time = models.CharField(max_length=10, null=True, default=None)
    days = models.ManyToManyField(Day)
    rating = models.DecimalField(null=True, default=None, max_digits=2, decimal_places=1)
    weight = models.IntegerField(null=True, default=None)
    image = models.URLField(null=True, default=None)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

    def getJSONVariant(self):
        genres = [genre.name for genre in getManyOrNone(self.genres)]
        days = [day.name for day in getManyOrNone(self.days)]

        return {
            'externalId': self.externalId,
            'name': self.name,
            'language': self.language,
            'genres': genres,
            'time': self.time,
            'days': days,
            'rating': self.rating,
            'weight': self.weight,
            'image': self.image,
            'channel': self.channel.getJSONVariant()
        }


class Episode(models.Model):
    externalId = models.IntegerField()
    name = models.CharField(max_length=200)
    season = models.IntegerField(null=True, default=None)
    number = models.IntegerField(null=True, default=None)
    startTime = models.DateTimeField(null=True, default=None)
    endTime = models.DateTimeField(null=True, default=None)
    rating = models.DecimalField(null=True, default=None, max_digits=2, decimal_places=1)
    image = models.URLField(null=True, default=None)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)

    def getJSONVariant(self):
        return {
            'externalId': self.externalId,
            'name': self.name,
            'season': self.season,
            'number': self.number,
            'startTime': getTimeString(self.startTime),
            'endTime': getTimeString(self.endTime),
            'rating': self.rating,
            'image': self.image,
            'show': self.show.getJSONVariant(),
        }
