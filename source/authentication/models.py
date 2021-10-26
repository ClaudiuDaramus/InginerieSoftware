from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# multi profile for one user
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creationDate = models.DateField(auto_now_add=True)
    profileName = models.CharField(max_length=20)
    # adding a default name in the create view
    # here we can save some history of the user metrics
