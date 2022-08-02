from django.db import models

class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    # project manager , group name
    group_name = models.CharField(max_length=200,default='task')
