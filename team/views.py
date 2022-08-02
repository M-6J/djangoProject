from django.shortcuts import render

# Create your views here.

from .models import Team

def detail(request,username):

    team = Team.objects.get(id=username)
    context = {'team': team}
    return render(request, 'team/team_detail.html', context)