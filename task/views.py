from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Task
from django.http import HttpResponseNotAllowed
from .forms import TaskForm

def index(request):
    task_list = Task.objects.order_by('-startdate')
    context = {'task_list': task_list}
    return render(request, 'task/task_list.html', context)

def detail(request, task_id):
    task = Task.objects.get(id=task_id)
    context = {'task': task}
    return render(request, 'task/task_detail.html', context)

def modify(request, task_id):
    if request.method == 'POST':
        task_name = request.POST['task_name']
        #worker = request.POST["worker"]
        status = request.POST['status']
        startdate = request.POST['startdate']
        task = Task(
            task_name=task_name,
            #worker=worker,
            status=status,
            startdate = startdate,
        )
        task.save()
        return redirect('/task/index')
    else:
        task = Task.objects.get(id=task_id)
        context = {'task': task}
        return render(request, 'task/task_modify.html', context)

def delete(request,task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('/')

def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.create_date = timezone.now()
            task.progress = 0
            task.save()
            return redirect('task:index')
    else:
        form = TaskForm()
    context = {'form': form}
    return render(request, 'task/task_form.html', context)