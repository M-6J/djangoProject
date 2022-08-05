import string

from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse

from profileApp.models import Notice
from taskApp.models import Task
from teamApp.models import Team, Member
import random


# ============================================= Managing Team Here From, ===============================================
# ===========================================  create, update, del, detail =============================================
def team_managing(request):
    """ -> team manage page
    GET, /team/manage
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
    username = request.GET.get('username')
    user = User.objects.get(username__exact=username)
    friends = User.objects.filter(profile__friend__exact=user)
    data = serializers.serialize('json', friends, fields='username')

    return HttpResponse(content=data)


def team_create(request):
    """ -> create team in team manage page (modal pop-up)
    POST, /team/create
    :param request: username(str，操作人员的用户名), team_name(str，团队名), description(str，团队说明), region(int，以后说),
                    member(str, 好友的用户名)
    :return: json   [
                        {"msg": "success"} or {"err code"}
                    ]
    """
    username = request.POST.get('username')  # to be creator
    self = User.objects.get(username__exact=username)

    creator = Member.objects.create(user=self, role=2)

    team_name = request.POST.get('team_name')
    description = request.POST.get('description')

    choice = request.POST.get('region')

    new_team = Team.objects.create(name=team_name, description=description, region=choice)
    new_team.member.add(creator)

    member = request.POST.getlist('member', None)

    for i in member:
        user = User.objects.get(username__exact=i)
        j = Member.objects.create(user=user, role=0)
        j.save()

        new_team.member.add(j)

    new_team.save()

    return JsonResponse({
        "msg": "success"
    })


def team_detail(request, pk):
    """ -> detail page for team
    GET, /team/detail/<int:pk>
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
                        {
                        }
                    [
                        {
                            "model": "auth.User",
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
                            "model": "taskApp.task",
                            "pk": (int),
                            "fields": {
                                "name": (str),
                                "description": (str),
                                "worker": (str),
                                "start": (datetime)
                                "ddl": (datetime)
                                "status": (int)
                                }
                        },
                        {
                            ... -> can be multiple objects
                        }
                    ]
    """
    team = Team.objects.get(pk=pk)

    detail = serializers.serialize('json', [team], fields=(
        'name', 'description', 'region'
    ))

    members = User.objects.filter(member__team__exact=team)
    member_list = serializers.serialize('json', members, fields=(
        'username', 'email'
    ))

    tasks = Task.objects.filter(team__exact=team)
    task_list = serializers.serialize('json', tasks, fields=(
        'name', 'description', 'worker', 'start', 'ddl'
    ))

    data = {
        detail,
        member_list,
        task_list
    }

    return HttpResponse(content=data)


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


def invite_member(request):  # add member by input: email
    """ -> invite member
    POST, /team/invite
    :param request: team_pk(int), sender(str，操作人员的用户名), rel_choice(str，是邮箱还是用户名), rel(str，那个值)
    :return: json   [
                        {"msg": "success"} or {"err code"}
                    ]
    """
    team = Team.objects.get(pk=request.POST.get('team_pk'))
    sender = User.objects.get(username__exact=request.POST.get('sender'))

    verify(team, sender, None, 1)

    rel_choice = request.POST.get('rel_choice')
    rel = request.POST.get('rel')

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


def del_member(request):  # quit or del member, quit: self, del: manager or creator
    """ -> delete member
    POST, /team/del
    :param request: team_pk(int), oper(str，操作人员的用户名), target(str，对象的用户名)
    :return: json   [
                        {"msg": "success"} or {"err code"}
                    ]
    """
    team = Team.objects.get(pk=request.POST.get('team_pk'))
    oper = User.objects.get(username__exact=request.POST.get('oper'))
    target = User.objects.get(username__exact=request.POST.get('target'))

    tar = verify(team, oper, target, 2)

    team.member.remove(tar)
    team.save()

    return JsonResponse({'msg': 'success'})


def promote(request):
    """ -> promote member (member -> manager)
    POST, /team/pro
    :param request: team_pk(int), oper(str，操作人员的用户名), target(str，对象的用户名)
    :return: json   [
                        {"msg": "success"} or {"err code"}
                    ]
    """
    team = Team.objects.get(pk=request.POST.get('team_pk'))
    oper = User.objects.get(username__exact=request.POST.get('oper'))
    target = User.objects.get(username__exact=request.POST.get('target'))

    tar = verify(team, oper, target, 2)

    if tar.model.role < 2:
        tar.model.role = tar.model.role + 1
        tar.model.save()
    else:
        return JsonResponse({'msg': 'err 104'})  # not allowed

    return JsonResponse({'msg': 'success'})


def degrade(request):
    """ -> degrade member (manager -> member)
    POST, team/deg
    :param request: team_pk(int), oper(str，操作人员的用户名), target(str，对象的用户名)
    :return: json   [
                        {"msg": "success"} or {"err code"}
                    ]
    """
    team = Team.objects.get(pk=request.POST.get('team_pk'))
    oper = User.objects.get(username__exact=request.POST.get('oper'))
    target = User.objects.get(username__exact=request.POST.get('target'))

    tar = verify(team, oper, target, 2)

    if tar.model.role > 0:
        tar.model.role = tar.model.role - 1
        tar.model.save()
    else:
        return JsonResponse({'msg': 'err 104'})
    return JsonResponse({'msg': 'success'})
