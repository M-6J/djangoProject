from django.urls import path

from profileApp.views import accept, signup, login

app_name = 'profileApp'

urlpatterns = [
    path('accept_invite/<str:verif>', accept, name='accept'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login')
]
