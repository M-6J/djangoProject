from django.forms import ModelForm

from teamApp.models import Team


class TeamCreationForm(ModelForm):

    class Meta:
        model = Team
        fields = ['name', 'description']
