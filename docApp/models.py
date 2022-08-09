from django.contrib.auth.models import User
from django.db import models

from projectApp.models import Project
from teamApp.models import Team


class Doc(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    content = models.TextField

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='docs_all')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='docs_proj')

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='docs_my')
    writers = models.ManyToManyField(User, blank=True, related_name='docs_lmy')

    last_modi = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
