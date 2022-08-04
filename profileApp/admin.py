from django.contrib import admin

# Register your models here.
from profileApp.models import Profile, Notice

admin.site.register(Profile)
admin.site.register(Notice)
