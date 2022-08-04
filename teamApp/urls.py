from django.urls import path

from teamApp.views import team_managing, team_create, team_detail, invite_member

app_name = 'teamApp'

urlpatterns = [
    path('manage/', team_managing, name='manage'),
    path('create/', team_create, name='create'),
    path('detail/<int:pk>', team_detail, name='detail'),
    path('invite/', invite_member, name='invite')
]
