from django.contrib.auth.models import User
from django.db import models


class Team(models.Model):
    # image = models.ImageField + url here
    name = models.CharField(max_length=30, null=False)
    description = models.TextField(max_length=200, null=True)

    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='own_team')
    manager = models.ManyToManyField(User, null=True, related_name='manage_team')
    member = models.ManyToManyField(User, null=False, related_name='team')
