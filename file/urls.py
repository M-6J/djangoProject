from django.urls import path
from .views import *

app_name = 'file'

urlpatterns = [
	path('filelist/', fileList, name="filelist"),
	path('<int:file_id>', fileDetail, name="filedetail"),
	path('fileupload/', fileUpload, name="fileupload"),
]