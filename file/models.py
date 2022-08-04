from django.db import models
from ckeditor.fields import RichTextField

class FileUpload(models.Model):
    title = models.TextField(max_length=40, null=True)
    file = models.FileField(null=True, upload_to="", blank=True)
    content = RichTextField(default='')
    writer = models.CharField(max_length=40, default='')
    startdate = models.DateTimeField()

    def __str__(self):
        return self.title