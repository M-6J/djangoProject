from django.urls import path

from . import views

app_name = 'task'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:task_id>/', views.detail, name='detail'),
    path('<int:task_id>/modify', views.modify, name='modify'),
    path('<int:task_id>/delete', views.delete, name='delete'),
    path('task/create/', views.task_create, name='task_create'),
]