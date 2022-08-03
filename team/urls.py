from django.urls import path

from . import views

app_name = 'team'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:team_id>/detail', views.detail, name='detail'),
    path('<int:team_id>/delete', views.delete, name='delete'),
    path('<int:team_id>/modify', views.modify, name='modify'),
]