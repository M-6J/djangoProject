from django.urls import path

from teamApp.views import *

app_name = 'teamApp'

urlpatterns = [
    path('req/', team_managing, name='manage'),
    path('create/', team_create, name='create')
]
