from django.forms import ModelForm
from .models import FileUpload
from ckeditor.widgets import CKEditorWidget
from django import forms

class FileUploadForm(ModelForm):
    content = forms.CharField(widget = CKEditorWidget())

    class Meta:
        model = FileUpload
        fields = '__all__'