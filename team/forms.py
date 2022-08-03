from django import forms
from .models import Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['team_name','description','managers','members','task']
        labels = {
            'team_name' : 'team_name',
            'managers' : 'managers',
            'members' : 'members',
            'task' : 'task',
            'description' : 'description',
        }

