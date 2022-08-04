from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    # profile image here, default none -> white image
    # profile description here, default none (text)
    description = models.TextField(max_length=200)
    # profile identity here, default none (char)
    identity = models.CharField(max_length=30)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    friend = models.ManyToManyField(User, blank=True, related_name='user')


class Notice(models.Model):
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='notice')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notice')
    content = models.TextField(null=False)
