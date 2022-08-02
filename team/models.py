from django.db import models

# Create your models here.
from user.models import User

class manager(models.Model):
    name = models.ForeignKey(User,on_delete=models.CASCADE)

class member(models.Model):
    member = models.ForeignKey(User,on_delete=models.CASCADE)


class team(models.Model):
    teamname = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    manager = models.ManyToManyField(manager)
    member = models.ManyToManyField(member)
    task = models.CharField(max_length=30)
