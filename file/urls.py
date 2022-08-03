from django.urls import path
from .views import *

app_name = 'file'

urlpatterns = [
	path('filelist/', fileList, name="filelist"),
	path('<int:file_id>', fileDetail, name="filedetail"),
	path('<int:file_id>/modify', fileModify, name="filemodify"),
	path('fileupload/', fileUpload, name="fileupload"),
]