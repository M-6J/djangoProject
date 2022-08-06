from django.urls import path

from projectApp.views import *

app_name = 'projectApp'

urlpatterns = [
    path('manage/', manage, name='manage'),
    path('create/', create, name='create'),
    path('detail/<int:pk>', detail, name='detail'),
    path('update/', update, name='update'),
    path('delete/', delete, name='delete')
]
