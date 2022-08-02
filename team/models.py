from django.db import models

# Create your models here.
from user.models import User

class Team(models.Model):
    team_name = models.CharField(max_length=30)
    description = models.CharField(max_length=30)

    managers = models.ManyToManyField(User, related_name='teams1')
    members = models.ManyToManyField(User, related_name='teams2')

    task = models.CharField(max_length=30)
