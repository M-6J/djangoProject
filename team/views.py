from django.shortcuts import render

# Create your views here.

from .models import Team

def detail(request):

    team_list = Team.objects.all()
    context = {'team_list': team_list}
    return render(request, 'team/team_detail.html', context)