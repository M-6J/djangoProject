from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from projectApp.models import Project
from teamApp.models import Member, Team


# =============================================== not completed yet ====================================================
# ============================================ has to be refactored, gn ================================================
def method_auth(request, method):
    if request.method == method:
        pass
    else:
        return JsonResponse({'msg': 'err 200'})


def check_null(pk):
    if Project.objects.filter(pk=pk).exists():
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


# ======================================================================================================================
# ======================================================================================================================
@csrf_exempt
def manage(request):  # -> loads project list where: team(pk=pk)
    """
    GET, /project/manage/
    :param request: team_pk(int) -> team_pk = team id
                    username(str) -> 操作人员的用户名
    :return: Json (project list)
    """
    method_auth(request, 'GET')

    team_pk = request.GET.get('team_pk', None)

    projects = Project.objects.filter(team_id__exact=team_pk)

    data = serializers.serialize('json', projects, fields=(
        'name'
    ))

    return HttpResponse('json', data)


@csrf_exempt
def detail(request, pk):  # read data in project where: project(pk=pk)
    """
    GET, /project/detail/<int:pk>/ -> pk = pk for project
    :param request:
    :param pk:  pk for project
    :return: Json (project's name and description)
    """
    method_auth(request, 'GET')

    project = Project.objects.get(pk=pk)

    check_null(pk)

    data = serializers.serialize('json', project, fields=(  # return fields of this project
        'name', 'description'
    ))

    return HttpResponse(content=data)


@csrf_exempt
def search(request, pk):
    """
    GET, /project/search/<int:pk> -> pk for team(pk=pk)
    :param request: search(str) -> 'Guan Jian Ci'
    :return: Json
    """
    method_auth(request, 'GET')

    search_words = request.GET['search']

    projects = Project.objects.filter(team_id=pk).filter(
        Q(name__icontains=search_words) | Q(description__icontains=search_words)
    )

    result = serializers.serialize('json', projects, fields=(
        'name', 'description'
    ))

    return HttpResponse(content=result)


# ======================================================================================================================
# ======================================================================================================================
@csrf_exempt
def create(request):  # -> create project where: team(pk=pk)
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
def update(request):  # update data in project where: project(pk=pk)
    """
    POST, /project/update/
    :param request: project_pk(int) ->  -> pk = pk for project
                    re_name(str), re_description(str)
                    username(str) -> 操作人员的用户名
    :return: Json (success or other)
    """
    method_auth(request, 'POST')

    data = json.loads(request.body)

    check_null(data.get('project_pk'))

    project = Project.objects.get(pk=data.get('project_pk'))

    project.name = data.get('re_name')
    project.description = data.get('re_description')
    project.save()

    return JsonResponse({'msg': 'success'})


@csrf_exempt
def delete(request):  # delete project where: project(pk=pk)
    """
    POST, /project/delete/
    :param request: project_pk(int) -> pk for project
                    username(str) -> 操作人员的用户名
    :return: Json (success or other)
    """
    method_auth(request, 'POST')

    data = json.loads(request.body)

    check_null(data.get('project_pk'))

    project = Project.objects.get(pk=data.get('project_pk'))

    project.delete()

    return JsonResponse({'msg': 'success'})


@csrf_exempt
def copy(request):
    """
    POST, /project/copy
    :param request: project_pk(int) -> pk for project(id=pk)
    :return: Json, {success or something err}
    """
    method_auth(request, 'POST')

    data = json.loads(request.body)

    check_null(data.get('project_pk'))

    origin = Project.objects.get(pk=data.get('project_pk'))

    copy_ = Project.objects.create(
        name=origin.name + '_copy',
        description=origin.description,
        team=origin.team
    )
    copy_.save()

    return JsonResponse({'msg': 'success'})
