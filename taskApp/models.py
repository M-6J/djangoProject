from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from teamApp.models import Team


class Task(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=200)

    # relationship below
    worker = models.ForeignKey(User, on_delete=models.SET_DEFAULT, null=True, default=None)
    workerName = models.CharField(max_length=50)

    # team = models.ForeignKey(Team, on_delete=models.CASCADE) --> project

    start = models.DateTimeField(null=True, default=None)
    ddl = models.DateTimeField(null=True, default=None)

    STATUS_CHOICES = (
        (0, 'ready for worker'),
        (1, 'worker exists'),
        (2, 'on work'),
        (3, 'err found'),
        (4, 'completed'),
        (5, 'garbage')
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
