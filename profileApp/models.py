from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    description = models.TextField(max_length=200)
    identity = models.CharField(max_length=30)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    friend = models.ManyToManyField(User, blank=True, related_name='user')


class Notice(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notice')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='noticee')
    content = models.TextField(max_length=60)
    team_pk = models.IntegerField
    verif = models.TextField(max_length=50)
