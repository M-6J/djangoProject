from django.conf import settings
from django.db import models


class Team(models.Model):
    # image = models.ImageField + url here
    name = models.CharField(max_length=30, null=False)
    description = models.TextField(max_length=200, null=True)

    member = models.ManyToManyField(to='Member', related_name='team')


class Member(models.Model):
    ROLE_CHOICES = (
        (0, 'member'),
        (1, 'manager'),
        (2, 'creator')
    )
    role = models.IntegerField(choices=ROLE_CHOICES, default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='member')
