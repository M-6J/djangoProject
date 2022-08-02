from django.urls import path

from . import views

app_name = 'project'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('project/create/', views.project_create, name='project_create'),
]