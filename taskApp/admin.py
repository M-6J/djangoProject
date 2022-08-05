from django.contrib import admin

# Register your models here.
from taskApp.models import Task

admin.site.register(Task)
