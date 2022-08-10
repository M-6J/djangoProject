import json

from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse

from django.views.decorators.csrf import csrf_exempt

from docApp.models import Doc
from projectApp.models import Project
from teamApp.models import Team, Member


def method_auth(request, method):
    if request.method == method:
        return 'pass'
    else:
        return 'method is not allowed'


def member_auth(user_pk, team_pk):
    user = User.objects.get(pk=user_pk)
    team = Team.objects.get(pk=team_pk)

    if Member.objects.filter(team__exact=team).filter(user__exact=user).exists():
        return 'pass'
    else:
        return 'user is not member'


def auth_(msg1, msg2):
    if msg1 is not 'pass':
        err = {'msg': msg1}
        return json.dumps(err)
    elif msg2 is not 'pass':
        err = {'msg': msg2}
        return json.dumps(err)
    else:
        return None


def jl(data):
    return json.loads(data)


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
    data = jl(request.body)
    user = User.objects.get(username__exact=data.get('username'))

    t = auth_(method_auth(request, 'POST'), member_auth(user.pk, data.get('team_pk')))

    if isinstance(t, str):
        return HttpResponse(content=t)

    doc = Doc.objects.create(
        title=data.get('title'),
        description=data.get('description'),
        contents=data.get('content'),

        team=Team.objects.get(pk=data.get('team_pk')),
        project=Project.objects.get(pk=data.get('project_pk')),

        author=User.objects.get(username__exact=user.username),
        last_modi=User.objects.get(username__exact=user.username),
    )

    doc.writers.add(User.objects.get(username__exact=user.username))
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
    data = jl(request.body)
    user = User.objects.get(username__exact=data.get('username'))

    t = auth_(method_auth(request, 'POST'), member_auth(user.pk, data.get('team_pk')))

    if isinstance(t, str):
        return HttpResponse(content=t)

    doc = Doc.objects.get(pk=data.get('doc_pk'))

    doc.title = data.get('title')
    doc.contents = data.get('content')
    doc.description = data.get('description')

    doc.writers.add(user)
    doc.last_modi = user

    doc.save()

    return JsonResponse({'msg': 'success'})


# ======================================================================================================================
# ======================================================================================================================
@csrf_exempt
def detail(request, pk):
    """
    GET, /docs/detail/<int:pk> -> pk for doc's id
    :param pk:
    :param request: username(str: 操作人用户名)
    :return: Json, doc's detail
    """
    msg1 = method_auth(request, 'GET')

    user = User.objects.get(username__exact=request.GET.get('username'))
    doc = Doc.objects.get(pk=pk)

    msg2 = member_auth(user.pk, doc.team.pk)

    t = auth_(msg1, msg2)

    if isinstance(t, str):
        return HttpResponse(content=t)

    data = {
        'title': doc.title,
        'description': doc.description,
        'content': doc.contents
    }

    result = json.dumps(data)

    return HttpResponse(content=result)


# ======================================================================================================================
# ======================================================================================================================
def serializer(docs):
    data = [{
        'pk': i.pk,
        'title': i.title,
        'description': i.description,
        'author': i.author.username,
        'last_writer': i.last_modi.username,
        'updated_at': i.updated_at
    } for i in docs]

    result = json.dumps(data, default=str)

    return result


@csrf_exempt
def teams(request, pk):
    """
    GET, /docs/list1/<int:pk> -> pk for team
    :param pk:
    :param request: username(str: 操作人用户名)
    :return: json, docs' list
    """
    msg1 = method_auth(request, 'GET')

    user = User.objects.get(username__exact=request.GET.get('username'))
    docs = Doc.objects.filter(team_id=pk)

    msg2 = member_auth(user.pk, pk)

    t = auth_(msg1, msg2)

    if isinstance(t, str):
        return HttpResponse(content=t)

    result = serializer(docs)

    return HttpResponse(content=result)


@csrf_exempt
def projects(request, pk):
    """
    GET, /docs/list2/<int:pk> -> pk for project
    :param pk:
    :param request: username(str: 操作人用户名)
    :return:
    """
    msg1 = method_auth(request, 'GET')

    user = User.objects.get(username__exact=request.GET.get('username'))
    team = Team.objects.get(project=Project.objects.get(pk=pk))

    docs = Doc.objects.filter(project_id=pk)

    msg2 = member_auth(user.pk, team.pk)

    t = auth_(msg1, msg2)

    if isinstance(t, str):
        return HttpResponse(content=t)

    result = serializer(docs)

    return HttpResponse(content=result)


@csrf_exempt
def my(request):
    """
    GET, /docs/list3/
    :param request: username(str: 操作人用户名)
    :return:
    """
    msg = method_auth(request, 'GET')

    if msg is not 'pass':
        t = jl({'err': msg})
        return HttpResponse(content=t)

    docs = Doc.objects.filter(writers=User.objects.get(username__exact=request.GET.get('username')))

    result = serializer(docs)

    return HttpResponse(content=result)
