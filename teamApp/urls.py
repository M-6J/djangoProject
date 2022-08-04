from django.urls import path

from teamApp.views import *

app_name = 'teamApp'

urlpatterns = [
    path('manage/', team_managing, name='manage'),
    path('create/', team_create, name='create'),
    path('detail/<int:pk>', team_detail, name='detail')
]
