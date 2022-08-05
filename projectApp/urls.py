from django.urls import path

from projectApp.views import *

app_name = 'projectApp'

urlpatterns = [
    path('manage/', manage, name='manage'),
    path('create/', create, name='create'),
    path('detail/', detail, name='detail'),
    path('update/', update, name='update'),
]
