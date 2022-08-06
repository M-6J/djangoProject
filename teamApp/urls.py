from django.urls import path

from teamApp.views import team_managing, team_create, team_detail, invite_member, del_member, promote, degrade, \
    team_list

app_name = 'teamApp'

urlpatterns = [
    path('manage/', team_managing, name='manage'),
    path('create/', team_create, name='create'),
    path('detail/<int:pk>', team_detail, name='detail'),
    path('invite/', invite_member, name='invite'),
    path('del/', del_member, name='deleteM'),
    path('pro/', promote, name='promoteM'),
    path('deg/', degrade, name='degradeM'),
    path('list/', team_list, name='list')
]
