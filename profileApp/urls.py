from django.urls import path

from profileApp.views import accept, signup, login, notice_view, add_friend

app_name = 'profileApp'

urlpatterns = [
    path('accept_invite/<str:verif>', accept, name='accept'),
    path('notices/', notice_view, name='notice'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),

    path('add/', add_friend, name='add')
]
