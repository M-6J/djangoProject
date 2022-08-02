from django import forms
from pybo.models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content', 'group_name']
        labels = {
            'subject': 'subject',
            'content': 'content',
            'group_name' : 'group_name',
        }
