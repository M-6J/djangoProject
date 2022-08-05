# from django.contrib.auth.models import User
# from django.http import JsonResponse
# from django.shortcuts import render
#
# from taskApp.models import Task
# from teamApp.models import Team
#
#
# def method_auth(request, method):
#     if request.method == method:
#         pass
#     else:
#         return JsonResponse({'msg': 'err 200'})
#
#
# def task_create(request):
#     method_auth(request, 'POST')
#
#     task = Task.objects.create(
#         name=request.POST.get('name'),
#         description=request.POST.get('description'),
#         team=Team.objects.get(pk=request.POST.get('team_pk')),
#         status=0
#     )
#     task.save()
#
#     return JsonResponse({'msg': 'success'})
#
#
# def task_edit(request):
#     method_auth(request, 'POST')
#
#     task = Task.objects.get(pk=request.POST.get('task_pk'))
#
#     pass
#
#
# def work(request):
#     method_auth(request, 'POST')
#
#     task = Task.objects.get(pk=request.POST.get('task_pk'))
#
#     worker = User.objects.get()


# ================================== Not now...
