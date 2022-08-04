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
    username = request.POST.get('username')
    user = User.objects.get(username__exact=username)
    friends = User.objects.filter(profile__friend__exact=user)
    data = serializers.serialize('json', friends, fields='username')

    return HttpResponse(content=data)


def team_create(request):
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
    team = Team.objects.get(pk=pk)

    detail = serializers.serialize('json', [team], fields=(
        'name', 'description', 'region'
    ))

    members = User.objects.filter(member__team__exact=team)
    member_list = serializers.serialize('json', members, fields=(
        'username'
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
def invite_member(request):  # add member by input: email
    team = Team.objects.get(pk=request.POST.get('team_pk'))
    sender = User.objects.get(username__exact=request.POST.get('sender'))

    a = Member.objects.filter(team__exact=team).filter(user__exact=sender)

    if a.exists():
        if a.model.role > 0:
            pass
        else:
            return JsonResponse({'msg': 'err 1001'})
    else:
        return JsonResponse({'msg': 'err 100'})

    rel_choice = request.POST.get('rel_choice')
    rel = request.POST.get('rel')

    if rel_choice == 'username':
        receiver = User.objects.get(username__exact=rel)
    elif rel_choice == 'email':
        receiver = User.objects.get(email__exact=rel)
    else:
        return JsonResponse({'msg': 'err 101'})

    if team.member.contains(receiver):
        return JsonResponse({'msg': 'err 102'})
    else:
        content = team.name
        target = team.pk

        verif = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(30))

        notice = Notice.objects.create(sender=sender, receiver=receiver, content=content, team_pk=target, verif=verif)
        notice.save()

        return JsonResponse({'msg': 'success'})


# add decorators here, 'creator, manager and self only' for post, get
def del_member(request):  # quit or del member, quit: self, del: manager or creator
    team = Team.objects.get(pk=request.GET.get('team_pk'))
    target = User.objects.get(email__exact=request.GET('target_user'))

    if team.member.contains(target):
        pass  # del target from member pool
    pass


# add decorators here, 'creator only' for post, get
def promote(request):
    team = Team.objects.get(pk=request.GET.get('team_pk'))
    if team.member.contains('value'):  # is contained for value
        target = User.objects.get(pk=request.GET('user_pk'))
        team.manager.add(target)
        team.save()
    else:
        return HttpResponseForbidden

    return  # return to team detail


# add decorators here, 'creator only' for post, get
def degrade(request):
    team = Team.objects.get(pk=request.GET('team_pk'))
    if team == request.user.own_team:
        team.delete()
    else:
        return HttpResponseForbidden

    return  # return to main
