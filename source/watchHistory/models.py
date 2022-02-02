from django.db import models

from authentication.models import Profile
from authentication.serializers import *

# Create your models here.
class WatchHistory(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    externalId = models.IntegerField()
    type = models.CharField(max_length=120)
    preference = models.BooleanField(blank=False, null=False)


    def __str__(self):
        return self.externalId

    def getJSONVariant(self):
        return  {
            "profile": ProfileSerializer.getJsonVariant(self.profile),
            "externalId": self.externalId,
            "type": self.type,
            "preference": self.preference
        }