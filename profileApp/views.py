from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse, HttpResponse

from profileApp.models import Notice, Profile
from teamApp.models import Team, Member


def method_auth(request, method):
    if request.method == method:
        pass
    else:
        return JsonResponse({'msg': 'err 200'})


def notice_view(request):
    """
    GET, /profile/notices
    :param request: username(str)
    :return: json   [
                        {
                            "model": "profileApp.Notice",
                            "pk": (int),
                            "fields": {
                                "sender": (str，发送该邀请的人员用户名),
                                "content": (str, 团队名),
                                "team_pk": (int, 团队的编号, 用于(/team/detail/<int:pk>)的pk)
                                "verif": (str, 用于承诺邀请的字符串, 链接(/profile/accept_invite/<str:verif>),就能承诺邀请
                                }
                        },
                        {
                            ... -> can be multiple objects
                        }
                    ]
    """

    method_auth(request, 'GET')

    profile = Profile.objects.get(user__username__exact=request.GET.get('username'))
    notices = Notice.objects.filter(receiver__profile__exact=profile)

    notice_list = serializers.serialize('Json', notices, fields=(
        'sender', 'content', 'team_pk', 'verif'
    ))

    return HttpResponse(content=notice_list)


def accept(request, verif):  # accept invite with verif code: verif code generated in teamApp invite
    """ -> accept invite, url is provided in notice_view (above api)
    POST, /profile/accept_invite/<str:verif>
    :param request:
    :param verif: provided above
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
            if User.objects.get(username__exact=request.POST.get('username')):
                return JsonResponse({'msg': 'err 201'})  # username duplicates
            user = User.objects.create_user(
                username=request.POST.get('username'),
                password=request.POST.get('password1'),
                email=request.POST.get('email')
            )
            auth.login(request, user)
            return JsonResponse({'msg': 'success'})
    else:
        return JsonResponse({'msg': 'err 200'})  # method err


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
            return JsonResponse({'msg': 'err 202'})  # username doesn't exist
    else:
        return JsonResponse({'msg': 'err 200'})

