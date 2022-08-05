from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

from projectApp.models import Project


def method_auth(request, method):
    if request.method == method:
        pass
    else:
        return JsonResponse({'msg': 'err 200'})


@csrf_exempt
def manage(request):
    method_auth(request, 'GET')
    pass


@csrf_exempt
def create(request):
    """
    POST, /project/create/
    :param request:
    :return:
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
    :param pk:
    :return:
    """
    method_auth(request, 'GET')

    project = Project.objects.get(pk=pk)

    data = serializers.serialize('Json', project, fields=(  # return fields of this project

    ))

    pass


@csrf_exempt
def update(request):
    method_auth(request, 'POST')

    data = json.loads(request.body)

    project = Project.objects.get(name__exact=data.get('name'))



    pass
