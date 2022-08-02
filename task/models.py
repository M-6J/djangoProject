from django.db import models

from user.models import User

class Task(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE)

    status = models.CharField(max_length=200)

    startdate = models.DateTimeField()
    enddate = models.DateTimeField()

    progress = models.IntegerField()
