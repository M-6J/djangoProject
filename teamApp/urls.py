from django.urls import path

from teamApp.views import *

app_name = 'teamApp'

urlpatterns = [
    path('create/', TeamCreateView.as_view(), name='create'),
    path('update/<int:pk>', TeamUpdateView.as_view(), name='update'),
    path('del/<int:pk>', del_team, name='del'),
    path('detail/<int:pk>', TeamDetailView.as_view(), name='detail')
]
