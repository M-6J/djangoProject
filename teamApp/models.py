from django.contrib.auth.models import User
from django.db import models


class Team(models.Model):
    REGION_CHOICES = (
        (0, 'need to select'),
        (1, 'Frontend Team'),
        (2, 'Backend Team'),
        (3, 'Fullstack Team'),
        (4, 'Devops Team'),
        (5, 'Marketing Team')
    )
    # image = models.ImageField + url here
    name = models.CharField(max_length=30, null=False)
    description = models.TextField(max_length=200, null=True)
    region = models.IntegerField(choices=REGION_CHOICES, default=0)

    member = models.ManyToManyField(to='Member', related_name='team')


class Member(models.Model):
    ROLE_CHOICES = (
        (0, 'member'),
        (1, 'manager'),
        (2, 'creator')
    )
    role = models.IntegerField(choices=ROLE_CHOICES, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='member')
