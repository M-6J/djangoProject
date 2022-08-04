from django.urls import path

from profileApp.views import accept

app_name = 'profileApp'

urlpatterns = [
    path('accept_invite/<str:verif>', accept, name='accept'),
]
