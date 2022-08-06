from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from projectApp.models import Project
from teamApp.models import Member, Team


def method_auth(request, method):
    if request.method == method:
        pass
    else:
        return JsonResponse({'msg': 'err 200'})


def member_auth(user_pk, team_pk):
    user = User.objects.get(pk=user_pk)
    team = Team.objects.get(pk=team_pk)

    if Member.objects.filter(team__exact=team).filter(user__exact=user).exists():
        pass
    else:
        return JsonResponse({'msg': 'err 501'})


@csrf_exempt
def manage(request):
    """
    GET, /project/manage/
    :param request: team_pk(int) -> team_pk = team id
                    username(str) -> 操作人员的用户名
    :return: Json (project list)
    """
    method_auth(request, 'GET')

    team_pk = request.GET.get('team_pk', None)

    projects = Project.objects.filter(team_id__exact=team_pk)

    data = serializers.serialize('Json', projects, fields=(
        'name'
    ))

    return HttpResponse('Json', data)


@csrf_exempt
def create(request):
    """
    POST, /project/create/
    :param request: project_name(str), description(str),
                    team_pk(int) -> team_pk = team id
                    username(str) -> 操作人员的用户名
    :return: Json (success or other)
    """
    method_auth(request, 'POST')

    data = json.loads(request.body)

    project = Project.objects.create(
        name=data.get('project_name'),
        description=data.get('description'),
        team_id=data.get('team_pk')
    )
    project.save()

    return JsonResponse({'msg': 'success'})


@csrf_exempt
def detail(request, pk):
    """
    GET, /project/detail/<int:pk>/ -> pk = pk for project
    :param request:
    :param pk:  pk for project
    :return: Json (project's name and description)
    """
    method_auth(request, 'GET')

    project = Project.objects.get(pk=pk)

    data = serializers.serialize('Json', project, fields=(  # return fields of this project
        'name', 'description'
    ))

    return HttpResponse(content=data)


@csrf_exempt
def update(request):
    """
    GET, /project/update/
    :param request: project_pk(int) ->  -> pk = pk for project
                    re_name(str), re_description(str)
                    username(str) -> 操作人员的用户名
    :return: Json (success or other)
    """
    method_auth(request, 'POST')

    data = json.loads(request.body)

    project = Project.objects.get(pk=data.get('project_pk'))

    project.name = data.get('re_name')
    project.description = data.get('re_description')
    project.save()

    return JsonResponse({'msg': 'success'})


@csrf_exempt
def delete(request):
    """
    POST, /project/delete/
    :param request: project_pk(int) -> pk for project
                    username(str) -> 操作人员的用户名
    :return: Json (success or other)
    """
    method_auth(request, 'POST')

    data = json.loads(request.body)

    project = Project.objects.get(pk=data.get('project_pk'))

    project.delete()

    return JsonResponse({'msg': 'success'})
