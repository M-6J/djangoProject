from django.urls import path

from docApp.views import *

app_name = 'docApp'

urlpatterns = [
    path('create/', create, name='create'),
    path('update/', update, name='update'),

    path('list1/<int:pk>', teams, name='teams_list'),
    path('list2/<int:pk>', projects, name='projects_list'),
    path('list3/', my, name='my_list'),

    path('detail/<int:pk>', detail, name='detail'),
]
