import json

from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

from docApp.models import Doc
from projectApp.models import Project
from teamApp.models import Team, Member


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


# ======================================================================================================================
# ======================================================================================================================
@csrf_exempt
def create(request):
    """
    POST, /docs/create/
    :param request: title(str), team_pk(int: id), project_pk(int: id), username(str: 操作人用户名), content(str),
                    description(str)
    :return: Json, {success or err code}
    """
    method_auth(request, 'POST')
    data = json.loads(request.body)
    user = User.objects.get(username__exact=data.get('username'))

    member_auth(user.pk, data.get('team_pk'))

    doc = Doc.objects.create(
        title=data.get('title'),
        description=data.get('description'),
        content=data.get('content'),

        team=Team.objects.get(pk=data.get('team_pk')),
        project=Project.objects.get(pk=data.get('project_pk')),

        author=User.objects.get(username__exact=user.username),
        writers=User.objects.get(username__exact=user.username),
        last_modi=User.objects.get(username__exact=user.username),
    )
    doc.save()

    return JsonResponse({'msg': 'success'})


@csrf_exempt
def update(request):
    """
    POST, /docs/update/
    :param request: title(str), doc_pk(int: id), team_pk(int: id), username(str: 操作人用户名), content(str),
                    description(str)
    :return: Json, {success or err code}
    """
    method_auth(request, 'POST')
    data = json.loads(request.body)
    user = User.objects.get(username__exact=data.get('username'))

    member_auth(user.pk, data.get('team_pk'))

    doc = Doc.objects.get(pk=data.get('doc_pk'))

    doc.title = data.get('title')
    doc.content = data.get('content')
    doc.description = data.get('description')

    doc.writers.add(user)
    doc.last_modi = user

    doc.save()

    return JsonResponse({'msg': 'success'})


# ======================================================================================================================
# ======================================================================================================================
# GET, detail of a doc
#   return: doc's detail (team name + pk, project name + pk, title, content, description, author, last modi,
#                         last update date)
@csrf_exempt
def detail(request, pk):
    """
    GET, /docs/detail/<int:pk> -> pk for doc's id
    :param request: username(str: 操作人用户名)
    :return: Json, doc's detail
    """
    method_auth(request, 'GET')

    doc = Doc.objects.get(pk=pk)

    # member_auth()

    data = {
        'title': doc.title,
        'description': doc.description,
        'content': doc.content
    }

    result = json.dumps(data)

    return HttpResponse(content=result)


# ======================================================================================================================
# ======================================================================================================================
@csrf_exempt
def teams(request, pk):
    """
    GET, /docs/list1/<int:pk> -> pk for team
    :param request: username(str: 操作人用户名)
    :return: json, docs' list
    """
    method_auth(request, 'GET')

    docs = Doc.objects.filter(team_id=pk)

    # member_auth()

    data = [{
        'pk': i.pk,
        'title': i.title,
        'description': i.description,
        'author': i.author.username,
        'last_writer': i.last_modi.username,
        'updated_at': i.updated_at
    } for i in docs]

    result = json.dumps(data)

    return HttpResponse(content=result)


@csrf_exempt
def projects(request, pk):
    """
    GET, /docs/list2/<int:pk> -> pk for project
    :param request: username(str: 操作人用户名)
    :return:
    """
    method_auth(request, 'GET')

    docs = Doc.objects.filter(project_id=pk)

    # member_auth()

    data = [{
        'pk': i.pk,
        'title': i.title,
        'description': i.description,
        'author': i.author.username,
        'last_writer': i.last_modi.username,
        'updated_at': i.updated_at
    } for i in docs]

    result = json.dumps(data)

    return HttpResponse(content=result)


@csrf_exempt
def my(request):
    """
    GET, /docs/list3/
    :param request: username(str: 操作人用户名)
    :return:
    """
    method_auth(request, 'GET')

    docs = Doc.objects.filter(writers=request.GET.get('username'))

    # member_auth()

    data = [{
        'pk': i.pk,
        'title': i.title,
        'description': i.description,
        'author': i.author.username,
        'last_writer': i.last_modi.username,
        'updated_at': i.updated_at
    } for i in docs]

    result = json.dumps(data)

    return HttpResponse(content=result)
