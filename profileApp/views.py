from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse

from profileApp.models import Notice
from teamApp.models import Team, Member


def accept(request, verif):  # accept invite with verif code: verif code generated in teamApp invite
    """ -> accept invite
    :param request: nothing
    :param verif:
    :return: Json   [
                        {'msg': 'success'} or {'errcode'}
                    ]
    """
    if Notice.objects.exists(verif__exact=verif):
        notice = Notice.objects.get(verif__exact=verif)
        target = Team.objects.get(pk=notice.team_pk)

        receiver = Member.objects.create(user=notice.receiver, role=0)

        target.member.add(receiver)
        target.save()

        notice.delete()

        return JsonResponse({'msg': 'success'})
    else:
        return JsonResponse({'msg': 'err 404'})


def signup(request):
    """ -> signup
    POST, /profile/signup
    :param request: username(str), password1(str), password2(str), email(str)
    :return: Json   [
                        {'msg': 'success'} or {'errcode'}
                    ]
    """
    if request.method == 'POST':
        if request.POST.get('password1') == request.POST.get('password2'):
            user = User.objects.create_user(
                username=request.POST.get('username'),
                password=request.POST.get('password1'),
                email=request.POST.get('email')
            )
            auth.login(request, user)
            return JsonResponse({'msg': 'success'})
    else:
        return JsonResponse({'msg': 'err 200'})


def login(request):
    """ -> login
    POST, /profile/login
    :param request: username(str), password(str)
    :return: Json   [
                        {'msg': 'success'} or {'errcode'}
                    ]
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return JsonResponse({'msg': 'success'})
        else:
            return JsonResponse({'msg': 'err 201'})
    else:
        return JsonResponse({'msg': 'err 200'})

