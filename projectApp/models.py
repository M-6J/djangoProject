from django.db import models

from teamApp.models import Team


class Project(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=255)

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='project')
