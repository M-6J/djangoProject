from django.urls import path

from projectApp.views import manage, create, detail, update, delete, copy, search

app_name = 'projectApp'

urlpatterns = [
    path('manage/', manage, name='manage'),  # loads list of project
    path('create/', create, name='create'),  # create project
    path('detail/<int:pk>', detail, name='detail'),  # read detail of project
    path('update/', update, name='update'),  # update project
    path('delete/', delete, name='delete'),  # delete project
    path('copy/', copy, name='copy'),  # copy project

    path('search/<int:pk>', search, name='search')
]
