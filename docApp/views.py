from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

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
# POST, create a doc
#   return: success or err code
@csrf_exempt
def create(request):
    """

    :param request:
    :return:
    """
    method_auth(request, 'POST')

    member_auth()
    pass


# POST, update a doc
#   return: success or err code
@csrf_exempt
def update(request):
    """

    :param request:
    :return:
    """
    method_auth(request, 'POST')

    member_auth()
    pass


# ======================================================================================================================
# ======================================================================================================================
# GET, detail of a doc
#   return: doc's detail (team name + pk, project name + pk, title, content, description, author, last modi,
#                         last update date)
@csrf_exempt
def detail(request):
    """

    :param request:
    :return:
    """
    method_auth(request, 'GET')

    member_auth()
    pass


# ======================================================================================================================
# ======================================================================================================================
# GET, list of docs - team's
#   return:
@csrf_exempt
def teams(request):
    """

    :param request:
    :return:
    """
    method_auth(request, 'GET')

    member_auth()
    pass


# GET, list of docs - projects'
#   return:
@csrf_exempt
def projects(request):
    """

    :param request:
    :return:
    """
    method_auth(request, 'GET')

    member_auth()
    pass


# GET, list of docs - my
#   return:
@csrf_exempt
def my(request):
    """

    :param request:
    :return:
    """
    method_auth(request, 'GET')

    member_auth()
    pass
