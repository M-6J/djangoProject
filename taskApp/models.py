from django.contrib.auth.models import User
from django.db import models

from teamApp.models import Team


class Task(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=200)

    # relationship below
    worker = models.ForeignKey(User, on_delete=models.SET_DEFAULT, null=True, default=None)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    start = models.DateTimeField(null=True, default=None)
    ddl = models.DateTimeField(null=True, default=None)

    status = models.CharField
