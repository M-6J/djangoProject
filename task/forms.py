from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name','worker', 'status']
        labels = {
            'task_name' : 'task_name',
            'worker': 'worker',
            'status': 'satus',
        }

