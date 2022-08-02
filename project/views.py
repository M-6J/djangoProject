from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Project
from django.http import HttpResponseNotAllowed
from .forms import ProjectForm

def index(request):
    question_list = Project.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'project/question_list.html', context)

def detail(request, question_id):
    question = Project.objects.get(id=question_id)
    context = {'question': question}
    return render(request, 'project/question_detail.html', context)

def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('project:index')
    else:
        form = ProjectForm()
    context = {'form': form}
    return render(request, 'project/project_form.html', context)