from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse

from profileApp.models import Notice
from taskApp.models import Task
from teamApp.models import Team, Member
import json


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
        "success": "success"
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
# add decorators here, 'creator and manager only' for post, get
def add_member(request):  # add member by input: email
    team = Team.objects.get(pk=request.POST.get('team_pk'))
    sender = User.objects.get(username__exact=request.POST.get('sender'))

    rel_choice = request.POST.get('rel_choice')

    if rel_choice == 'username':
        receiver = User.objects.get(username__exact=rel_choice)
    elif rel_choice == 'email':
        receiver = User.objects.get(email__exact=rel_choice)

    Notice.objects.create()

    target = User.objects.get(email__exact=request.POST.get('target_user'))

    if team.member.contains(target):
        pass  # already invited! and just redirect to member managing url
    else:
        pass  # send complete!
    # send notice to user, you are invited to team -> this link: add user to member, and member redirect to team detail.
    pass


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
    if team == request.user.own_team:
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
