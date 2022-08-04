from django.contrib import admin

# Register your models here.
from teamApp.models import Team, Member

admin.site.register(Team)
admin.site.register(Member)
