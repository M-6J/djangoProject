import json
import random
import string

from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from profileApp.models import Notice
from projectApp.models import Project
from teamApp.models import Team, Member


def method_auth(request, method):
    if request.method == method:
        pass
    else:
        return JsonResponse({'msg': 'err 200'})


# ============================================= Managing Team Here From, ===============================================
# ===========================================  create, update, del, detail =============================================
@csrf_exempt
def team_managing(request):
    """ -> team manage page
    GET, /team/manage/
    :param request: username(str，操作人员的用户名)
    :return: json   [
                        {
                            "model": "auth.User",
                            "pk": (int),
                            "fields": {
                                "username": (str，好友的用户名，用于新建团队的信息)
                                }
                        },
                        {
                            ... -> can be multiple objects
                        }
                    ]
    """

    method_auth(request, 'GET')

    username = request.GET.get('username', None)

    if username is None:
        return JsonResponse({'msg': 'need login'})

    user = User.objects.get(username__exact=username)
    friends = User.objects.filter(profile__friend__exact=user)
    data = serializers.serialize('json', friends, fields='username')

    return HttpResponse(content=data)


@csrf_exempt
def team_list(request):
    """
    GET, team/list/
    :param request: username(str，操作人员的用户名)
    :return: ..
    """

    method_auth(request, 'GET')

    username = request.GET.get('username')

    teams = Team.objects.filter(member__user__username=username)

    if not teams.exists():
        return JsonResponse({'msg': 'no teams you joined'})

    data = serializers.serialize('json', teams, fields=(
        'team', 'name', 'description', 'region', 'member'
    ))

    return HttpResponse(content=data)


@csrf_exempt
def team_create(request):
    """ -> create team in team manage page (modal pop-up)
    POST, /team/create/
    :param request: username(str，操作人员的用户名), team_name(str，团队名), description(str，团队说明), region(int，以后说),
                    "members":  [   -> members = Json list
                                    {"member“: "好友一的用户名"}, -> member(str, 那个好友的用户名)
                                    {"member": "好友二的用户名"},
                                    . . .
                                ]
    :return: json   [
                        {"msg": "success"} or {"err code"}
                    ]
    """

    method_auth(request, 'POST')

    data = json.loads(request.body)

    username = data.get('username')  # to be creator 1
    self = User.objects.get(username__exact=username)

    creator = Member.objects.create(user=self, role=2)

    team_name = data.get('team_name')
    description = data.get('description')

    choice = data.get('region')

    new_team = Team.objects.create(name=team_name, description=description, region=choice)
    new_team.member.add(creator)

    members = data.get('members')

    for i in members:
        user = User.objects.get(username__exact=i['member'])
        j = Member.objects.create(user=user, role=0)
        j.save()

        new_team.member.add(j)

    new_team.save()

    return JsonResponse({
        "msg": "success"
    })


@csrf_exempt
def team_detail(request, pk):
    """ -> detail page for team
    GET, /team/detail/<int:pk>/
    :param request: none
    :param pk: for teamApp.team
    :return: json   [
                        {
                            "model": "teamApp.team",
                            "pk": (int),
                            "fields": {
                                "name": (str),
                                "description": (str),
                                "region": (int)
                                }
                        }
                    ]
                    [
                        {
                            "model": "auth.user",
                            "pk": (int),
                            "fields": {
                                "username": (str)
                                }
                        },
                        {
                            ... -> can be multiple objects
                        }
                    ]
                    [
                        {
                            "model": "projectApp.project",
                            "pk": (int),
                            "fields": {
                                "name": (str),
                                "description": (str)
                                }
                        },
                        {
                            ... -> can be multiple objects
                        }
                    ]
    """

    method_auth(request, 'GET')

    team = Team.objects.get(pk=pk)

    detail = serializers.serialize('json', [team], fields=(
        'name', 'description', 'region'
    ))

    members = User.objects.filter(member__team__exact=team)
    member_list = serializers.serialize('json', members, fields=(
        'username', 'email'
    ))

    projects = Project.objects.filter(team__exact=team)
    project_list = serializers.serialize('json', projects, fields=(
        'name', 'description'
    ))

    d1 = json.loads(detail)
    d2 = json.loads(member_list)
    d3 = json.loads(project_list)

    context = {
        'detail': d1,
        'members': d2,
        'projects': d3
    }

    dt = json.dumps(context, indent=2)

    return HttpResponse(content=dt)


# ============================================ Managing Members Here From, =============================================
# =========================================  add, del(quit), promote, degrade ==========================================
def verify(team, oper, targ, typ):
    temp = Member.objects.filter(team__exact=team).filter(user__exact=oper)
    tar = Member.objects.filter(team__exact=team).filter(user__exact=targ)

    if typ == 1:  # invite
        if temp.exists() | temp.model.role > 0:
            pass
    elif typ == 2:  # delete
        if not tar.exists():
            return JsonResponse({'msg': 'err 103'})  # already deleted
        elif temp.exists() | temp.model.role > tar.model.role:
            return tar
    else:
        return JsonResponse({'msg': 'err 100'})  # authority error


@csrf_exempt
def invite_member(request):  # add member by input: email
    """ -> invite member
    POST, /team/invite/
    :param request: team_pk(int), sender(str，操作人员的用户名), rel_choice(str，是邮箱还是用户名), rel(str，那个值)
    :return: json   [
                        {"msg": "success"} or {"err code"}
                    ]
    """

    method_auth(request, 'POST')

    data = json.loads(request.body)

    team = Team.objects.get(pk=data.get('team_pk'))
    sender = User.objects.get(username__exact=data.get('sender'))

    verify(team, sender, None, 1)

    rel_choice = data.get('rel_choice')
    rel = data.get('rel')

    if rel_choice == 'username':
        receiver = User.objects.get(username__exact=rel)
    elif rel_choice == 'email':
        receiver = User.objects.get(email__exact=rel)
    else:
        return JsonResponse({'msg': 'err 101'})  # method error

    if team.member.contains(receiver):
        return JsonResponse({'msg': 'err 102'})  # already member
    else:
        content = team.name
        target = team.pk

        verif = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(30))

        notice = Notice.objects.create(sender=sender, receiver=receiver, content=content, team_pk=target, verif=verif)
        notice.save()

        return JsonResponse({'msg': 'success'})


@csrf_exempt
def del_member(request):  # quit or del member, quit: self, del: manager or creator
    """ -> delete member
    POST, /team/del/
    :param request: team_pk(int), oper(str，操作人员的用户名), target(str，对象的用户名)
    :return: json   [
                        {"msg": "success"} or {"err code"}
                    ]
    """

    method_auth(request, 'POST')

    data = json.loads(request.body)

    team = Team.objects.get(pk=data.get('team_pk'))
    oper = User.objects.get(username__exact=data.get('oper'))
    target = User.objects.get(username__exact=data.get('target'))

    tar = verify(team, oper, target, 2)

    team.member.remove(tar)
    team.save()

    return JsonResponse({'msg': 'success'})


@csrf_exempt
def promote(request):
    """ -> promote member (member -> manager)
    POST, /team/pro/
    :param request: team_pk(int), oper(str，操作人员的用户名), target(str，对象的用户名)
    :return: json   [
                        {"msg": "success"} or {"err code"}
                    ]
    """

    method_auth(request, 'POST')

    data = json.loads(request.body)

    team = Team.objects.get(pk=data.get('team_pk'))
    oper = User.objects.get(username__exact=data.get('oper'))
    target = User.objects.get(username__exact=data.get('target'))

    tar = verify(team, oper, target, 2)

    if tar.model.role < 2:
        tar.model.role = tar.model.role + 1
        tar.model.save()
    else:
        return JsonResponse({'msg': 'err 104'})  # not allowed

    return JsonResponse({'msg': 'success'})


@csrf_exempt
def degrade(request):
    """ -> degrade member (manager -> member)
    POST, /team/deg/
    :param request: team_pk(int), oper(str，操作人员的用户名), target(str，对象的用户名)
    :return: json   [
                        {"msg": "success"} or {"err code"}
                    ]
    """

    method_auth(request, 'POST')

    data = json.loads(request.body)

    team = Team.objects.get(pk=data.get('team_pk'))
    oper = User.objects.get(username__exact=data.get('oper'))
    target = User.objects.get(username__exact=data.get('target'))

    tar = verify(team, oper, target, 2)

    if tar.model.role > 0:
        tar.model.role = tar.model.role - 1
        tar.model.save()
    else:
        return JsonResponse({'msg': 'err 104'})
    return JsonResponse({'msg': 'success'})
