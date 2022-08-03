from django.shortcuts import render, redirect

# Create your views here.

from .models import Team

def index(request):

    team_list = Team.objects.all()
    context = {'team_list': team_list}
    return render(request, 'team/team_list.html', context)

def detail(request,team_id):
    team = Team.objects.get(id=team_id)
    context = {'team': team}
    return render(request, 'team/team_detail.html',context)

def delete(request,team_id):
    team = Team.objects.get(id=team_id)
    team.delete()
    return redirect('/team')

def modify(request,team_id):
    team = Team.objects.get(id=team_id)
    context = {'team': team}
    return render(request,'team/team_modify.html',context)