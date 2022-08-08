from django.db import models

from teamApp.models import Team


class Project(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=255)

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='project')

    created_at = models.DateTimeField(auto_now_add=True)  # -> created when
    updated_at = models.DateTimeField(auto_now=True)  # -> updated when

    # docs = models.ManyToManyField()

    # -> add some fields related: UML, docs, ...
    """
    UML -> X
    
    =============== WAIT ================
    
    Docs -> ~ Team, Project, My ...
    : ManyToMany Field, yield in parent
    """

